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
            if f'{year}' not in os.listdir():
                os.mkdir(f'{year}')

            os.chdir(f'{year}')
            if 'PDFs' not in os.listdir():
                os.mkdir('PDFs')

            if 'CSVs' not in os.listdir():
                os.mkdir('CSVs')

            os.chdir('..')

        os.chdir('..')

def scrape(competitions, max_year):
    start_scrape = time()
    with open('number_of_games.json', 'r') as f:
        n_games = json.load(f)

    errors = {}
    for competition in competitions:
        competition, cod = competition
        errors[competition] = {}
        for year in range(2013, max_year + 1):
            clear()
            print(f'Iniciando ano de {year} para {competition.replace("_", " ")} (scrape)')
            files = glob(f'{competition}/{year}/CSVs/*.csv')
            year = str(year)
            errors[competition][year] = []
            count_end = 0
            for game in range(1, n_games[competition][year]):
                if count_end == 10:
                    break
                    
                save = False
                try:
                    name = f'{competition}/{year}/PDFs/{str(game).zfill(3)}.pdf'
                    if name.replace('PDFs', 'CSVs').replace('pdf', 'csv') in files:
                        count_end = 0
                        continue

                    pdf = requests.get(f'https://conteudo.cbf.com.br/sumulas/{year}/{cod}{game}se.pdf').content
                    if b'File or directory not found' in pdf:
                        errors[competition][year].append(name)
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
                    if save:
                        name = name.replace('PDFs', 'CSVs')
                        name = name.replace('pdf', 'csv')
                        errors[competition][year].append(name)
                    else:
                        errors[competition][year].append(name)

    with open('Errors/scrape_errors.json', 'w') as f:
        json.dump(errors, f)

    end_scrape = time()
    return start_scrape, end_scrape

def extract(competitions, max_year):
    start_extract = time()
    with open('number_of_games.json', 'r') as f:
        n_games = json.load(f)

    errors = {}
    cont_sucess = 0
    cont_fail = 0
    for competition in competitions:
        competition = competition[0]
        for year in range(2013, max_year + 1):
            clear()
            print(f'Iniciando o ano de {year} para {competition.replace("_", " ")} (extração)')
            games = {}
            count_end = 0
            for game in range(1, n_games[competition][str(year)] + 1):
                if count_end == 10:
                    break
                    
                f_club, f_result, f_players, f_goals, f_changes = False, False, False, False, False
                try:
                    file = f'{competition}/{str(year)}/CSVs/{str(game).zfill(3)}.csv'
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
                    assert len(players) >= 36
                    f_players = True
                
                    goals = catch_goals(text)
                    assert len(goals) == int(result[0]) + int(result[-1])
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
                    erro = 'scrape'
                    if competition in errors:
                        if f'{year}' in errors[competition]:
                            errors[competition][f'{year}'][str(game).zfill(3)] = erro
                        else:
                            errors[competition][f'{year}'] = {}
                            errors[competition][f'{year}'][str(game).zfill(3)] = erro
                    else:
                        errors[competition] = {}
                        errors[competition][f'{year}'] = {}
                        errors[competition][f'{year}'][str(game).zfill(3)] = erro
                    
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
                        if f'{year}' in errors[competition]:
                            errors[competition][f'{year}'][str(game).zfill(3)] = erro
                        else:
                            errors[competition][f'{year}'] = {}
                            errors[competition][f'{year}'][str(game).zfill(3)] = erro
                    else:
                        errors[competition] = {}
                        errors[competition][f'{year}'] = {}
                        errors[competition][f'{year}'][str(game).zfill(3)] = erro

            with open(f'{competition}/{str(year)}/games.json', 'w') as f:
                json.dump(games, f)
                    
    with open('Errors/infos_errors.json', 'w') as f:
        json.dump(errors, f)
    
    end_extract = time()
    return start_extract, end_extract, cont_fail, cont_sucess

max_year = 2022
competitions = [('CdB', '424'),
                ('Serie_A', '142'),
                ('Serie_B', '242'),
                ('Serie_C', '342'),
                ('Serie_D', '542')]

make_directories(competitions, max_year)
start_scrape, end_scrape = scrape(competitions, max_year)
start_extract, end_extract, cont_fail, cont_sucess = extract(competitions, max_year)

clear()
print(f'Scrape finalizado em {end_scrape - start_scrape:.2f} segundos!',
      f'Extração finalizada em {end_extract - start_extract:.2f} segundos!',
      f'{cont_sucess} jogos foram extraídos com sucesso.',
      f'{cont_fail} jogos falharam.',
      '',
      '----------------------------------------',
      f'Tempo total: {end_extract - start_scrape:.2f} segundos.',
      sep = '\n')
      