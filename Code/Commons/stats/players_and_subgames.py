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
        players.append([[] for i in range(len(competitions))])
        sub_games_count.append([0 for i in range(len(competitions))])
    else:
        players.append(deepcopy(players[-1]))
        sub_games_count.append(sub_games_count[-1].copy())
    
    for i in range(len(competitions)):
        if i > 0:
            sub_games_count[2022 - year][i] = sub_games_count[2022 - year][i]
            players[2022 - year][i] = players[2022 - year][i].copy()
            
        competition = competitions[i]
        with open(f'../../Scrape/{competition}/{year}/squads.json', 'r') as f:
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
header = [item.replace('_', ' ').replace('Serie', 'Série') for item in header]
print(tabulate(players, headers = header, tablefmt = 'latex'))
print()
print(tabulate(sub_games_count, headers = header, tablefmt = 'latex'))
