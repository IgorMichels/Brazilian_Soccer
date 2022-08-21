from multiprocessing import Process
from functions import *
from glob import glob
from time import time
import requests
import json
import csv
import os

from PyPDF2 import *

def clear():
    os.system('clear')

def make_directories(competitions, max_year):
    for competition in competitions:
        name, cod = competition
        if name not in os.listdir():
            os.mkdir(name)

        os.chdir(name)
        for year in range(2013, max_year + 1):
            year = str(year)
            if year not in os.listdir():
                os.mkdir(year)

            os.chdir(year)
            if 'PDFs' not in os.listdir():
                os.mkdir('PDFs')

            if 'CSVs' not in os.listdir():
                os.mkdir('CSVs')

            os.chdir('..')

        os.chdir('..')

def extract_games(competition, cod, year, n_max, files, exceptions):
    count_end = 0
    for game in range(1, n_max):
	    if str(game).zfill(3) in exceptions[competition][year]:
	        continue
	    
	    if count_end == 10:
	        break
	    
	    try:
	        name = f'{competition}/{year}/PDFs/{str(game).zfill(3)}.pdf'
	        if name.replace('PDFs', 'CSVs').replace('pdf', 'csv') in files:
	            count_end = 0
	            continue
            
	        pdf = get_pdf(f'https://conteudo.cbf.com.br/sumulas/{year}/{cod}{game}se.pdf')
	        if b'File or directory not found' in pdf:
	            count_end += 1
	            continue

	        with open(name, 'wb') as f:
	            f.write(pdf)
	            save = True
	            count_end = 0

	        reader = PdfReader(name)
	        doc = []
	        for i in range(len(reader.pages)):
	            page = reader.pages[i]
	            doc += page.extract_text().split('\n')

	        for i in range(len(doc)):
	            doc[i] = [doc[i]]

	        name = name.replace('PDFs', 'CSVs')
	        name = name.replace('pdf', 'csv')
	        with open(name, 'w') as f:
	            write = csv.writer(f)
	            write.writerows(doc)

	    except:
	        pass

def get_pdf(url):
    return requests.get(url).content

def scrape(competitions, max_year, files, max_time = 10):
    with open('number_of_games.json', 'r') as f:
        n_games = json.load(f)
    
    with open('exceptions.json', 'r') as f:
        exceptions = json.load(f)

    errors = {}
    for competition in competitions:
        competition, cod = competition
        errors[competition] = {}
        for year in range(2013, max_year + 1):
            clear()
            print(f'Iniciando ano de {year} para {competition.replace("_", " ")} (scrape)')
            year = str(year)
            errors[competition][year] = []
            p = Process(target = extract_games, args = (competition, cod, year, n_games[competition][year], files, exceptions))
            p.start()
            p.join(max_time)
            p.terminate()

def extract(competitions, max_year):
    with open('number_of_games.json', 'r') as f:
        n_games = json.load(f)
    
    with open('exceptions.json', 'r') as f:
        exceptions = json.load(f)

    errors = {}
    cont_sucess = 0
    cont_fail = 0
    for competition in competitions:
        competition = competition[0]
        for year in range(2013, max_year + 1):
            clear()
            year = str(year)
            print(f'Iniciando o ano de {year} para {competition.replace("_", " ")} (extração)')
            games = {}
            count_end = 0
            for game in range(1, n_games[competition][str(year)] + 1):
                if str(game).zfill(3) in exceptions[competition][year]:
                    if exceptions[competition][year][str(game).zfill(3)] != {}:
                        games[str(game).zfill(3)] = exceptions[competition][year][str(game).zfill(3)]
                        
                    cont_sucess += 1
                    continue
                
                if count_end == 10:
                    break
                    
                f_club, f_result, f_players, f_goals, f_changes = False, False, False, False, False
                try:
                    file = f'{competition}/{year}/CSVs/{str(game).zfill(3)}.csv'
                    f = open(file)
                    data = f.readlines()
                    f.close()
                    text = ''
                    for row in data:
                        text += row
                    
                    clubs = catch_teams(text)
                    assert len(clubs) == 1
                    f_club = True
                
                    result = final_result(text)
                    assert len(result) == 1
                    result = result[0]
                    f_result = True
                
                    players = catch_players(text)
                    assert len(players) >= 28
                    f_players = True
                
                    goals = catch_goals(text)
                    aux = result.upper().split('X')
                    assert len(goals) == int(aux[0].strip()) + int(aux[-1].strip())
                    f_goals = True
                
                    changes = find_changes(text)
                    assert len(changes) <= 10
                    f_changes = True
                
                    games[str(game).zfill(3)] = {'Mandante'      : clubs[0][0],
                                                 'Visitante'     : clubs[0][1],
                                                 'Resultado'     : result,
                                                 'Jogadores'     : players,
                                                 'Gols'          : goals,
                                                 'Substituições' : changes}

                    cont_sucess += 1
                    count_end = 0
                except FileNotFoundError:
                    count_end += 1
                except AssertionError:
                    cont_fail += 1
                    if not f_club:
                        erro = 'clube'
                    elif not f_result:
                        erro = 'resultado'
                    elif not f_players:
                        erro = 'jogadores'
                    elif not f_goals:
                        erro = 'gols'
                    elif not f_changes:
                        erro = 'substituições'
                    else:
                        erro = 'ver'
                    if competition in errors:
                        if year in errors[competition]:
                            errors[competition][year][str(game).zfill(3)] = erro
                        else:
                            errors[competition][year] = {}
                            errors[competition][year][str(game).zfill(3)] = erro
                    else:
                        errors[competition] = {}
                        errors[competition][year] = {}
                        errors[competition][year][str(game).zfill(3)] = erro

            with open(f'{competition}/{year}/games.json', 'w') as f:
                json.dump(games, f)
                    
    with open('Errors/infos_errors.json', 'w') as f:
        json.dump(errors, f)
    
    return cont_fail, cont_sucess

def catch_squads(competitions, max_year):
    with open('number_of_games.json', 'r') as f:
        n_games = json.load(f)
    
    with open('exceptions.json', 'r') as f:
        exceptions = json.load(f)

    errors = {}
    cont_sucess = 0
    cont_fail = 0
    squads = {}
    for competition in competitions:
        competition = competition[0]
        squads[competition] = {}
        for year in range(2013, max_year + 1):
            clear()
            year = str(year)
            print(f'Iniciando o ano de {year} para {competition.replace("_", " ")} (escalações)')
            squads[competition][year] = {}
            with open(f'{competition}/{year}/games.json') as f:
                games = json.load(f)
            
            for game in games:
                if games[game] == {}:
                    continue
                
                players = games[game]['Jogadores']
                changes = games[game]['Substituições']
                goals = games[game]['Goals']
                for change in changes:
                    if ' / ' not in change:
                        if ' /' in change:
                            change = change.replace(' /', ' / ')
                        elif '/ ' in change:
                            change = change.replace('/ ', ' / ')
                        elif '/' in change:
                            change = change.replace('/', ' / ')
                    
                    change = treat_club(change)
            
    

if __name__ == '__main__':
    max_year = 2022
    competitions = [('CdB', '424'),
                    ('Serie_A', '142'),
                    ('Serie_B', '242'),
                    ('Serie_C', '342'),
                    ('Serie_D', '542')]

    make_directories(competitions, max_year)

    start_scrape = time()
    n = len(glob('*/*/CSVs/*.csv'))
    max_time = 10
    added = 0
    it = 1
    k = 0
    while n != k:
        files = glob('*/*/CSVs/*.csv')
        k = len(files)
        if it == 1:
            scrape(competitions, max_year, files, max_time)
        else:
            scrape(competitions, max_year, files, max_time / 2)
    
        n = len(glob('*/*/CSVs/*.csv'))
        added += n - k
        it += 1
        
    end_scrape = time()

    added = 1
    if added > 0:
        start_extract = time()
        cont_fail, cont_sucess = extract(competitions, max_year)
        end_extract = time()
        clear()
        print(f'Scrape finalizado em {end_scrape - start_scrape:.2f} segundos!',
              f'Extração finalizada em {end_extract - start_extract:.2f} segundos!',
              f'{added} jogos foram adicionados a base.',
              f'As informações de {cont_sucess} jogos foram extraídas com sucesso.',
              f'{cont_fail} jogos falharam ao extrair as informações.',
              '-' * 58,
              f'Tempo total: {end_extract - start_scrape:.2f} segundos.',
              sep = '\n')
    else:
        clear()
        print(f'Scrape finalizado em {end_scrape - start_scrape:.2f} segundos!',
              'Nenhum jogo foi adicionado a base.',
              sep = '\n')
