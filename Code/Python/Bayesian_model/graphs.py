import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

data = '22B'
df_1 = pd.read_csv(f'parameters_std_normal_prior_{data}_part_1.csv')
df_2 = pd.read_csv(f'parameters_std_normal_prior_{data}_part_2.csv')
df = pd.concat([df_1, df_2], ignore_index = True)
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
    defesa = df[f'theta_2.{player}'].values
    plt.hist(ataque, density = True, alpha = 0.7, label = 'Ataque')
    #plt.hist(defesa, density = True, alpha = 0.7, label = 'Defesa')
    plt.axvline(ataque.mean(), color = colors[0], linestyle = 'dashed', linewidth = 1, label = 'Ataque (média)')
    #plt.axvline(defesa.mean(), color = colors[1], linestyle = 'dashed', linewidth = 1, label = 'Defesa (média)')
    plt.title(name)
    plt.legend()
    plt.savefig(name + '.png')
    plt.show()
