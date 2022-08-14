from glob import glob
from time import time
import requests
import json
import csv
import os

from PyPDF2 import *

start = time()
#os.chdir('Área de Trabalho/FGV/00 - TCC/Scrape/')
competitions = [('Serie_A', '142'),
                ('Serie_B', '242'),
                ('Serie_C', '342'),
                ('Serie_D', '542'),
                ('CdB', '424')]

for competition in competitions:
    name, cod = competition
    if name not in os.listdir():
        os.mkdir(name)

    os.chdir(name)
    for year in range(2013, 2023):
        if f'{year}' not in os.listdir():
            os.mkdir(f'{year}')

        os.chdir(f'{year}')
        if 'PDFs' not in os.listdir():
            os.mkdir('PDFs')

        if 'CSVs' not in os.listdir():
            os.mkdir('CSVs')

        os.chdir('..')

    os.chdir('..')

with open('number_of_games.json', 'r') as f:
    games = json.load(f)

errors = {}
for competition in competitions:
    competition, cod = competition
    errors[competition] = {}
    for year in range(2013, 2023):
        print(f'Iniciando ano de {year} para {competition.replace("_", " ")}')
        files = glob(f'{competition}/{year}/CSVs/*.csv')
        year = str(year)
        errors[competition][year] = []
        for game in range(1, games[competition][year]):
            save = False
            try:
                name = f'{competition}/{year}/PDFs/{str(game).zfill(3)}.pdf'
                if name.replace('PDFs', 'CSVs').replace('pdf', 'csv') in files:
                    continue

                pdf = requests.get(f'https://conteudo.cbf.com.br/sumulas/{year}/{cod}{game}se.pdf').content
                if b'File or directory not found' in pdf:
                    errors[competition][year].append(name)
                    continue

                with open(name, 'wb') as f:
                    f.write(pdf)
                    save = True

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

        print(f'Finalizado ano de {year} para {competition.replace("_", " ")}\n')

with open('scrape_errors.json', 'w') as f:
    json.dump(errors, f)

end = time()
print(f'Scrape finalizado em {end - start:.2f} segundos!')
