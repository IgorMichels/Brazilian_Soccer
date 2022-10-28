import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

data = '21B'
df_1 = pd.read_parquet(f'home_away_model/parameters_std_normal_prior_{data}_home_away_part_1.parquet')
df_2 = pd.read_parquet(f'home_away_model/parameters_std_normal_prior_{data}_home_away_part_2.parquet')
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
    ataque_m = df[f'theta_atk_m.{player}'].values
    ataque_v = df[f'theta_atk_v.{player}'].values
    ataque_m_avg = ataque_m.mean()
    ataque_v_avg = ataque_v.mean()
    plt.hist(ataque_m, density = True, alpha = 0.7, label = 'Ataque - mandante')
    plt.hist(ataque_v, density = True, alpha = 0.7, label = 'Ataque - visitante')
    plt.axvline(ataque_m_avg, color = colors[0], linestyle = 'dashed',
                linewidth = 1, label = f'Ataque - mandante (média): {ataque_m_avg:.2f}')
    
    plt.axvline(ataque_v_avg, color = colors[1], linestyle = 'dashed',
                linewidth = 1, label = f'Ataque - visitante (média): {ataque_v_avg:.2f}')
    
    plt.title(name)
    plt.legend()
    # plt.savefig(name + 'ataque.png')
    plt.show()
    
    defesa_v = df[f'theta_def_v.{player}'].values
    defesa_m = df[f'theta_def_m.{player}'].values
    defesa_m_avg = defesa_m.mean()
    defesa_v_avg = defesa_v.mean()
    plt.hist(defesa_m, density = True, alpha = 0.7, label = 'Defesa - mandante')
    plt.hist(defesa_v, density = True, alpha = 0.7, label = 'Defesa - visitante')
    plt.axvline(defesa_m_avg, color = colors[0], linestyle = 'dashed',
                linewidth = 1, label = f'Defesa - mandante (média): {defesa_m_avg:.2f}')
    
    plt.axvline(defesa_v_avg, color = colors[1], linestyle = 'dashed',
                linewidth = 1, label = f'Defesa - visitante (média): {defesa_v_avg:.2f}')
    
    plt.title(name)
    plt.legend()
    # plt.savefig(name + 'defesa.png')
    plt.show()
