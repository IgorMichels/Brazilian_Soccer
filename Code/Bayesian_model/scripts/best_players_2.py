import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from glob import glob
from tabulate import tabulate
from itertools import product

if __name__ == '__main__':
    with open('../stats/best_players.txt', 'r') as f:
        best_players = f.readlines()[2:]
    
    for i, row in enumerate(best_players):
        row = row.split()
        model, model_year, *players = row
        for j, player in enumerate(players):
            info = None
            for year, div in product(range(22, int(model_year) - 1, - 1), ['A', 'B']):
                with open(f'../../../Scrape/results/Serie_{div}/{2000 + year}/games.json', 'r') as f:
                    data = json.load(f)
                    
                for game in data:
                    for game_player in data[game]['Jogadores']:
                        if player in game_player[0]:
                            info = (div, year, game, player, game_player[1], game_player[0])
                            break
                            
                    if info != None: break
                if info != None: break
            
            players[j] = info
        best_players[i] = [model, model_year, *players]
        
    for row in best_players:
        print(f'Modelo: {row[0]}')
        print(f'Ano: {row[1]}')
        print('Jogadores:')
        for player in row[2:]:
           print('  ', player)
        
        print()
