from tabulate import tabulate
from copy import deepcopy

import matplotlib.pyplot as plt
import json
import os

competitions = ['Serie_A', 'Serie_B', 'Serie_C', 'Serie_D', 'CdB']
players = []
sub_games_count = []
for year in range(2022, 2012, -1):
    if year == 2022:
        players.append([[], [], [], [], []])
        sub_games_count.append([0, 0, 0, 0, 0])
    else:
        players.append(deepcopy(players[-1]))
        sub_games_count.append(sub_games_count[-1].copy())
    
    for i in range(5):
        if i > 0:
            sub_games_count[2022 - year][i] = sub_games_count[2022 - year][i]
            players[2022 - year][i] = players[2022 - year][i].copy()
            
        competition = competitions[i]
        with open(f'../../../Scrape/{competition}/{year}/squads.json', 'r') as f:
            squads = json.load(f)
        
        for game in squads:
            for substituition in squads[game]:
                sub_games_count[2022 - year][i] += 1
                for player in squads[game][substituition]['Mandante']:
                    if player not in players[2022 - year][i]:
                        players[2022 - year][i].append(player)
                        
                for player in squads[game][substituition]['Visitante']:
                    if player not in players[2022 - year][i]:
                        players[2022 - year][i].append(player)

for i in range(len(players)):
    for j in range(len(players[i]) - 1, -1, -1):
        aux = []
        for k in range(j + 1):
            aux += players[i][k]
    
        players[i][j] = len(set(aux))
        sub_games_count[i][j] = sum(sub_games_count[i][:j + 1])
        
    players[i].insert(0, 2022 - i)
    sub_games_count[i].insert(0, 2022 - i)

header = ['Ano'] + competitions
header = [item.replace('_', ' ') for item in header]
print(tabulate(players, headers = header, tablefmt = 'latex'))
print()
print(tabulate(sub_games_count, headers = header, tablefmt = 'latex'))

'''
years = [*range(2022, 2012, -1)]
players_sub_games = [len(players[i]) / sub_games_count[i] for i in range(len(players))]
plt.plot(years, players_sub_games, color = 'blue', label = 'Jogadores por subpartida')
plt.legend()
plt.show()
'''

'''
fig, ax1 = plt.subplots()
ax1.plot(years, players_games, color = 'red', label = 'Jogadores por jogo')
ax1.set_xlabel('Ano')
ax1.set_ylabel('Jogadores por jogo')

ax2 = ax1.twinx()
ax2.plot(years, players_sub_games, color = 'blue', label = 'Jogadores por subpartida')

plt.ylabel('Jogadores por subpartida')
fig.legend(loc = 'upper right', bbox_to_anchor = (1, 1), bbox_transform = ax1.transAxes)
plt.title('Dados gerais')
plt.show()
'''
