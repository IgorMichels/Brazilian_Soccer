import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('parameters_std_normal_prior.csv')
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

    plt.hist(df[f'theta_1.{player}'], density = True)
    plt.title(name + ' (ataque)')
    plt.show()
    
    plt.hist(df[f'theta_2.{player}'], density = True)
    plt.title(name + ' (defesa)')
    plt.show()
