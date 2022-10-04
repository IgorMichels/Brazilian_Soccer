from tabulate import tabulate
import matplotlib.pyplot as plt
import json
import os

competitions = ['Serie_A', 'Serie_B', 'Serie_C', 'Serie_D', 'CdB']
players = [[], [], [], [], []]
sub_games_count = [[], [], [], [], []]

for i in range(5):
    for year in range(2022, 2012, -1):
        if year == 2022:
            players[i].append([])
            sub_games_count[i].append(0)
        else:
            players[i].append(players[i][-1].copy())
            sub_games_count[i].append(sub_games_count[i][-1])
        
        for competition in competitions[:i + 1]:
            with open(f'../../Scrape/{competition}/{year}/squads.json', 'r') as f:
                squads = json.load(f)
            
            for game in squads:
                for substituition in squads[game]:
                    sub_games_count[i][-1] += 1
                    for player in squads[game][substituition]['Mandante']:
                        if player not in players[i][-1]:
                            players[i][-1].append(player)
                            
                    for player in squads[game][substituition]['Visitante']:
                        if player not in players[i][-1]:
                            players[i][-1].append(player)
    
    players[i] = [competition] + [len(players[i][j]) for j in range(len(players[i]))]
    sub_games_count[i] = [competition] + sub_games_count[i]
    
years = ['Anos'] + [*range(2022, 2012, -1)]
print(tabulate(players, headers = years, tablefmt = 'latex'))
print()
print(tabulate(sub_games_count, headers = years, tablefmt = 'latex'))

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
