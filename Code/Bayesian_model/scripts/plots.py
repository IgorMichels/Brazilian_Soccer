import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from glob import glob
from itertools import product

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

def plot_distribuition(players, model = 'ADM', base = 18, atk = True, dim = (2, 2), show = True, save_name = 'players_distribuitions'):
    for year in range(base, 23):
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
        
        if atk:
            cols = []
            for column in df.columns:
                if 'atk' not in column: continue
                for player in players:
                    if column == f'theta_atk.{players_id[player[0]]}':
                        cols.append(column)
                    if column == f'theta_atk_m.{players_id[player[0]]}':
                        cols.append(column)
                    if column == f'theta_atk_v.{players_id[player[0]]}':
                        cols.append(column)
        
            df = df[cols]
            max_atk = int(np.max(np.max(df))) + 1
            bins = np.linspace(0, max_atk, 10 * max_atk + 1)
        else:
            cols = []
            for column in df.columns:
                if 'def' not in column: continue
                for player in players:
                    if column == f'theta_def.{players_id[player[0]]}':
                        cols.append(column)
                    elif column == f'theta_def_m.{players_id[player[0]]}':
                        cols.append(column)
                    elif column == f'theta_def_v.{players_id[player[0]]}':
                        cols.append(column)
        
            df = df[cols]
            max_def = int(np.max(np.max(df))) + 1
            bins = np.linspace(0, max_def, int(max_def / 5) + 1)

        fig, ax = plt.subplots(dim[0], dim[1], figsize = (10, 9), sharex = 'all', sharey = 'all')
        ax = ax.ravel()
        for i, player in enumerate(players):
            player, name = player
            player = players_id[player]
            if atk:
                if model == 'HAM1':
                    ax[i].hist(df[f'theta_atk_m.{player}'].values, alpha = 0.7, bins = bins)
                    atk_force = df[f'theta_atk_m.{player}'].values.mean()
                    ax[i].axvline(atk_force, color = colors[0], linestyle = 'dashed',
                                  linewidth = 1, label = f'Ataque (média mandante): {atk_force:.2f}')
                                  
                    ax[i].hist(df[f'theta_atk_v.{player}'].values, color = colors[2], alpha = 0.7, bins = bins)
                    atk_force = df[f'theta_atk_v.{player}'].values.mean()
                    ax[i].axvline(atk_force, color = colors[2], linestyle = 'dashed',
                                  linewidth = 1, label = f'Ataque (média visitante): {atk_force:.2f}')
                else:
                    ax[i].hist(df[f'theta_atk.{player}'].values, alpha = 0.7, bins = bins)
                    atk_force = df[f'theta_atk.{player}'].values.mean()
                    ax[i].axvline(atk_force, color = colors[0], linestyle = 'dashed',
                                  linewidth = 1, label = f'Ataque (média): {atk_force:.2f}')
            else:
                if model == 'HAM1':
                    ax[i].hist(df[f'theta_def_m.{player}'].values, color = colors[1], alpha = 0.7, bins = bins)
                    def_force = df[f'theta_def_m.{player}'].values.mean()
                    ax[i].axvline(def_force, color = colors[1], linestyle = 'dashed',
                                  linewidth = 1, label = f'Defesa (média mandante): {def_force:.2f}')
                    
                    ax[i].hist(df[f'theta_def_v.{player}'].values, color = colors[3], alpha = 0.7, bins = bins)
                    def_force = df[f'theta_def_v.{player}'].values.mean()
                    ax[i].axvline(def_force, color = colors[3], linestyle = 'dashed',
                                  linewidth = 1, label = f'Defesa (média visitante): {def_force:.2f}')
                else:
                    ax[i].hist(df[f'theta_def.{player}'].values, color = colors[1], alpha = 0.7, bins = bins)
                    def_force = df[f'theta_def.{player}'].values.mean()
                    ax[i].axvline(def_force, color = colors[1], linestyle = 'dashed',
                                  linewidth = 1, label = f'Defesa (média): {def_force:.2f}')

            ax[i].set_title(f'{name}')
            ax[i].legend(loc = 'upper right')

        fig.suptitle(f'Distribuições - 20{data[:2]} a 2022')
        if atk: plt.savefig(f'../plots/{save_name}_{data}_{model}_atk.png')
        else: plt.savefig(f'../plots/{save_name}_{data}_{model}_def.png')
        if show: plt.show()
        plt.close()

if __name__ == '__main__':
    players_def = [
                   ['392224', 'Murilo - Palmeiras'],
                   ['633571', 'Gustavo Gómez - Palmeiras'],
                   ['172367', 'David Luiz - Flamengo'],
                   ['310373', 'Léo Pereira - Flamengo']
                  ]
              
    players_atk = [
                   ['691654', 'Cano - Fluminense'],
                   ['291738', 'Dudu - Palmeiras'],
                   ['303716', 'Pedro - Flamengo'],
                   ['337830', 'Gabigol - Flamengo']
                  ]
    
    for model, atk in product(['ADM', 'HAM1', 'HAM2'], [True, False]):
        print(model, atk)
        plot_distribuition(players_atk, model = model, atk = atk, show = False, save_name = 'atk_players')
        plot_distribuition(players_def, model = model, atk = atk, show = False, save_name = 'def_players')
