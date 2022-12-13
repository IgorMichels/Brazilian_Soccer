import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from glob import glob
from itertools import product

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

def plot_distribuition(players, model = 'ADM', base = 18, prof = 'atk', dim = (1, 1), show = True, save_name = 'players_distribuitions'):
    for year in range(base, base + 1):
        data = f'{year}B'
        df = pd.DataFrame()
        for file_name in sorted(glob(f'../results/{model}/{data}*.parquet')):
            aux = pd.read_parquet(file_name)
            df = pd.concat([df, aux])
        
        players_file = f'../../Commons/players_{data}_all.json'
        with open(players_file, 'r') as f:
            players_id = json.load(f)

        if model == 'HAM1': avg = df[f'theta_atk_m.{players_id[players[0][0]]}'].values.mean()
        else: avg = df[f'theta_atk.{players_id[players[0][0]]}'].values.mean()
        for column in df.columns:
            df[column] = df[column] / avg
        
        cols = []
        for column in df.columns:
            if prof not in column: continue
            for player in players:
                if column == f'theta_{prof}.{players_id[player[0]]}': cols.append(column)
                if column == f'theta_{prof}_m.{players_id[player[0]]}': cols.append(column)
                if column == f'theta_{prof}_v.{players_id[player[0]]}': cols.append(column)
    
        df = df[cols]
        max_prof = int(np.max(np.max(df))) + 1
        bins = np.linspace(0, max_prof, 10 * max_prof + 1)
        for i, player in enumerate(players):
            player, name = player
            player = players_id[player]
            if model == 'HAM1':
                plt.hist(df[f'theta_{prof}_m.{player}'].values, color = colors[i], alpha = 0.7, bins = bins)
                prof_force = df[f'theta_{prof}_m.{player}'].values.mean()
            else:
                plt.hist(df[f'theta_{prof}.{player}'].values, color = colors[i], alpha = 0.7, bins = bins)
                prof_force = df[f'theta_{prof}.{player}'].values.mean()
            
            plt.axvline(prof_force, color = colors[i], linestyle = 'dashed',
                        linewidth = 1, label = f'{name} (média): {prof_force:.2f}')

        plt.legend(loc = 'upper right')
        if model == 'HAM1': plt.savefig(f'../plots/{save_name}_{data}_{model}_{prof}_home.png')
        else: plt.savefig(f'../plots/{save_name}_{data}_{model}_{prof}.png')
        if show: plt.show()
        plt.close()
        
        if model != 'HAM1': return
        # avg = df[f'theta_atk_v.{players_id[players[0][0]]}'].values.mean()
        # for column in df.columns:
        #     df[column] = df[column] / avg
        
        for i, player in enumerate(players):
            player, name = player
            player = players_id[player]
            plt.hist(df[f'theta_{prof}_v.{player}'].values, color = colors[i], alpha = 0.7, bins = bins)
            prof_force = df[f'theta_{prof}_v.{player}'].values.mean()
            plt.axvline(prof_force, color = colors[i], linestyle = 'dashed',
                        linewidth = 1, label = f'{name} (média): {prof_force:.2f}')

        plt.legend(loc = 'upper right')
        plt.savefig(f'../plots/{save_name}_{data}_{model}_{prof}_away.png')
        if show: plt.show()
        plt.close()

if __name__ == '__main__':
    players_atk = [
                   ['691654', 'Cano - Fluminense'],
                   ['303716', 'Pedro - Flamengo']
                  ]
    
    for model, prof in product(['ADM', 'HAM1', 'HAM2'], ['atk']):
        print(model, prof)
        plot_distribuition(players_atk, model = model, prof = prof, save_name = 'strikers', show = False)
