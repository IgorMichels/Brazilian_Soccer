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
    model = 'HAM2'
    years = range(18, 23)
    for year in years:
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
        
        results = results['sigma_atk'] * results['sigma_def']
        results = np.argsort(results)
        best = list(results[- n_best:])
        clubs_file = f'../../Commons/clubs_{data}.json'
        with open(clubs_file, 'r') as f:
            clubs_id = json.load(f)
        
        for club in clubs_id:
            if clubs_id[club] in best:
                ind = best.index(clubs_id[club])
                best[ind] = club
                break
        
        best = [model, year] + best
        table.append(best.copy())
    
    print(tabulate(table, headers = headers))
