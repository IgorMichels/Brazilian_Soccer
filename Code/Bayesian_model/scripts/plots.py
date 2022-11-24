import os
import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from glob import glob
from itertools import product

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

def plot_distribuition(player, models = ['ADM', 'HAM1', 'HAM2'], model_data = '18B', dim = (1, 3), show = True, save_name = None):
    players_file = f'../../Commons/players_{model_data}_all.json'
    with open(players_file, 'r') as f:
        player_id = json.load(f)
        player_id = player_id[player[0]]
    
    columns = [f'theta_atk.{player_id}', f'theta_def.{player_id}']
    for i, model in enumerate(models):
        df = pd.DataFrame()
        for file_name in sorted(glob(f'../results/{model}/{model_data}*.parquet')):
            aux = pd.read_parquet(file_name)
            df = pd.concat([df, aux])
        
        del aux
        if model == 'HAM1':
            df1 = df[[f'theta_atk_m.{player_id}', f'theta_def_m.{player_id}']]
            df2 = df[[f'theta_atk_v.{player_id}', f'theta_def_v.{player_id}']]
            df1.columns = columns
            df2.columns = columns
            df = pd.concat([df1, df2], ignore_index = True)
            del df1
            del df2
        
        data = df[columns]
        data.columns = ['Ataque', 'Defesa']
        data.reset_index(drop = True, inplace = True)
        sns.jointplot(data = data, x = 'Ataque', y = 'Defesa')
        plt.savefig(f'../plots/{model}_{player[0]}.png')
        # plt.show()
        plt.close()
        del data
        del df

if __name__ == '__main__':
    players = [
               ['565315', 'Sornoza - Corinthians'],
               ['152788', 'Wellington - América/MG'],
               ['691654', 'Cano - Fluminense'],
               ['291738', 'Dudu - Palmeiras'],
               ['303716', 'Pedro - Flamengo'],
               ['337830', 'Gabigol - Flamengo'],
               ['392224', 'Murilo - Palmeiras'],
               ['633571', 'Gustavo Gómez - Palmeiras'],
               ['172367', 'David Luiz - Flamengo'],
               ['310373', 'Léo Pereira - Flamengo']
              ]
    
    for player in players:
        plot_distribuition(player)
