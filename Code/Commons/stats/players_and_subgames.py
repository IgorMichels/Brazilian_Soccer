from tabulate import tabulate
from copy import deepcopy

import matplotlib.pyplot as plt
import json
import os

competitions = ['Serie_A', 'Serie_B', 'Serie_C', 'Serie_D', 'CdB']
players = []
sub_games_count = []
correlated_players = []
for year in range(2022, 2012, -1):
    if year == 2022:
        players.append([[] for i in range(len(competitions))])
        sub_games_count.append([0 for i in range(len(competitions))])
        correlated_players.append([{} for i in range(len(competitions))])
    else:
        players.append(deepcopy(players[-1]))
        sub_games_count.append(sub_games_count[-1].copy())
        correlated_players.append(deepcopy(correlated_players[-1]))
    
    for i, competition in enumerate(competitions):
        if i > 0:
            sub_games_count[2022 - year][i] = deepcopy(sub_games_count[2022 - year][i - 1])
            players[2022 - year][i] = players[2022 - year][i - 1].copy()
            correlated_players[2022 - year][i] = deepcopy(correlated_players[2022 - year][i - 1])
            
        with open(f'../../../Scrape/results/{competition}/{year}/squads.json', 'r') as f:
            squads = json.load(f)
        
        for game in squads:
            for substituition in squads[game]:
                sub_games_count[2022 - year][i] += 1
                
                for player in squads[game][substituition]['Mandante']:
                    if player not in players[2022 - year][i]: players[2022 - year][i].append(player)
                    
                    if player not in correlated_players[2022 - year][i]: correlated_players[2022 - year][i][player] = []
                    for player_2 in squads[game][substituition]['Mandante']:
                        if player_2 == player: continue
                        if player_2 not in correlated_players[2022 - year][i][player]:
                            correlated_players[2022 - year][i][player].append(player_2)
                            
                    for player_2 in squads[game][substituition]['Visitante']:
                        if player_2 == player: continue
                        if player_2 not in correlated_players[2022 - year][i][player]:
                            correlated_players[2022 - year][i][player].append(player_2)
                        
                for player in squads[game][substituition]['Visitante']:
                    if player not in players[2022 - year][i]: players[2022 - year][i].append(player)
                    
                    if player not in correlated_players[2022 - year][i]: correlated_players[2022 - year][i][player] = []
                    for player_2 in squads[game][substituition]['Mandante']:
                        if player_2 == player: continue
                        if player_2 not in correlated_players[2022 - year][i][player]:
                            correlated_players[2022 - year][i][player].append(player_2)
                            
                    for player_2 in squads[game][substituition]['Visitante']:
                        if player_2 == player: continue
                        if player_2 not in correlated_players[2022 - year][i][player]:
                            correlated_players[2022 - year][i][player].append(player_2)

for i in range(len(players)):
    for j in range(len(players[i])):
        players[i][j] = len(players[i][j])
        
        cont = 0
        for player in correlated_players[i][j]:
            cont += len(correlated_players[i][j][player])
            
        correlated_players[i][j] = cont // 2
        
    players[i].insert(0, 2022 - i)
    sub_games_count[i].insert(0, 2022 - i)
    correlated_players[i].insert(0, 2022 - i)

header = ['Ano'] + competitions
header = [item.replace('_', ' ').replace('Serie', 'Série') for item in header]
print(tabulate(players, headers = header, tablefmt = 'latex'))
print()
print(tabulate(sub_games_count, headers = header, tablefmt = 'latex'))
print()
print(tabulate(correlated_players, headers = header, tablefmt = 'latex'))

