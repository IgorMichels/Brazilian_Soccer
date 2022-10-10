import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

df = pd.read_csv('parameters_std_normal_prior_20B.csv')
players = [
           ['303716', 'Pedro - Flamengo'],
           ['502361', 'Pedro Raul - Goiás'],
           ['169050', 'Weverton - Palmeiras'],
           ['384823', 'Cleiton - Bragantino'],
           ['159238', 'Diego Alves - Flamengo']
          ]

with open('players.json', 'r') as f:
    players_id = json.load(f)

for player in players:
    player, name = player
    player = players_id[player]
    ataque = df[f'theta_1.{player}'].values
    defesa = df[f'theta_2.{player}'].values
    plt.hist(ataque, density = True, alpha = 0.7, label = 'Ataque')
    plt.hist(defesa, density = True, alpha = 0.7, label = 'Defesa')
    plt.axvline(ataque.mean(), color = colors[0], linestyle = 'dashed', linewidth = 1, label = 'Ataque (média)')
    plt.axvline(defesa.mean(), color = colors[1], linestyle = 'dashed', linewidth = 1, label = 'Defesa (média)')
    plt.title(name)
    plt.legend()
    plt.show()
