import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

data = '21B'
df = pd.read_parquet(f'atk_def_model/parameters_std_normal_prior_{data}.parquet')
players = [
           ['303716', 'Pedro - Flamengo'],
           ['502361', 'Pedro Raul - Goiás'],
           #['169050', 'Weverton - Palmeiras'],
           #['384823', 'Cleiton - Bragantino'],
           #['159238', 'Diego Alves - Flamengo'],
           ['337830', 'Gabigol - Flamengo'],
           ['691654', 'Cano - Fluminense']
          ]

players_file = f'../Commons/players_{data}_all.json'
with open(players_file, 'r') as f:
    players_id = json.load(f)

for player in players:
    player, name = player
    player = players_id[player]
    ataque = df[f'theta_1.{player}'].values
    ataque_avg = ataque.mean()
    plt.hist(ataque, density = True, alpha = 0.7, label = 'Ataque')
    plt.axvline(ataque_avg, color = colors[0], linestyle = 'dashed',
                linewidth = 1, label = f'Ataque (média): {ataque_avg:.2f}')
        
    plt.title(name)
    plt.legend()
    # plt.savefig(name + 'ataque.png')
    plt.show()
    
    defesa = df[f'theta_2.{player}'].values
    defesa_avg = defesa.mean()
    plt.hist(defesa, density = True, alpha = 0.7, label = 'Defesa')
    plt.axvline(defesa_avg, color = colors[0], linestyle = 'dashed',
                linewidth = 1, label = f'Defesa (média): {defesa_avg:.2f}')
    
    plt.title(name)
    plt.legend()
    # plt.savefig(name + 'defesa.png')
    plt.show()
