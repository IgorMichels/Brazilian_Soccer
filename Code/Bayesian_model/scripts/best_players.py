import json
import numpy as np
import pandas as pd

from glob import glob
from tabulate import tabulate
from itertools import product

if __name__ == '__main__':
    n_best = 10
    min_games = 100
    headers = ['Modelo', 'Ano'] + [str(i + 1) for i in range(n_best)]
    table = []
    models = ['ADM', 'HAM1', 'HAM2']
    years = range(18, 23)
    with open('../../Commons/stats/games_played.json', 'r') as f:
        games_played = json.load(f)
    
    for model, year in product(models, years):
        results = {}
        data = f'{year}B'
        players_file = f'../../Commons/players_{data}_all.json'
        with open(players_file, 'r') as f:
            players_id = json.load(f)
        
        players, ids = list(players_id.keys()), list(players_id.values())
        df = pd.DataFrame()
        for file_name in sorted(glob(f'../results/{model}/{data}*.parquet')):
            aux = pd.read_parquet(file_name)
            df = pd.concat([df, aux])
        
        df = df.describe().loc['mean']
        for row in df.index[7:]:
            if row.split('.')[0] not in results:
                results[row.split('.')[0]] = []
                
            results[row.split('.')[0]].append(df.loc[row])
        
        for key in results:
            results[key] = np.array(results[key])
        
        if model == 'HAM1':
            results = (results['theta_atk_v'] + results['theta_atk_v']) * (results['theta_def_m'] + results['theta_def_v']) / 4
        else:
            results = results['theta_atk'] * results['theta_def']
        
        results = np.argsort(results)
        best = []
        ind = 0
        while len(best) < n_best:
            player_id = results[ind]
            loc = ids.index(player_id)
            player = players[loc]
            if games_played[player] >= min_games:
                best.append(player)
                
            ind += 1
        
        best = [model, year] + best
        table.append(best.copy())
    
    for i, row in enumerate(table):
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
        table[i] = [model, model_year, *players]
        
    for row in table:
        print(f'Modelo: {row[0]}')
        print(f'Ano: {row[1]}')
        print('Jogadores:')
        for player in row[2:]:
           print('  ', player)
        
        print()
