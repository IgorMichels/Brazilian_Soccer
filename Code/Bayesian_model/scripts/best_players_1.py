import json
import numpy as np
import pandas as pd

from glob import glob
from tabulate import tabulate
from itertools import product

if __name__ == '__main__':
    n_best = 10
    headers = ['Modelo', 'Ano'] + [str(i + 1) for i in range(n_best)]
    table = []
    models = ['ADM', 'HAM1', 'HAM2']
    years = range(18, 23)
    for model, year in product(models, years):
        results = {}
        data = f'{year}B'
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
        
        if model == 'HAM1': results = (results['theta_atk_v'] + results['theta_atk_v']) * (results['theta_def_m'] + results['theta_def_v']) / 4
        else: results = results['theta_atk'] * results['theta_def']
        results = np.argsort(results)
        best = list(results[- n_best:])
        players_file = f'../../Commons/players_{data}_all.json'
        with open(players_file, 'r') as f:
            players_id = json.load(f)
        
        for player in players_id:
            if players_id[player] in best:
                ind = best.index(players_id[player])
                best[ind] = player
        
        best = [model, year] + best
        table.append(best.copy())
    
    print(tabulate(table, headers = headers))
