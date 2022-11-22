from tabulate import tabulate
import matplotlib.pyplot as plt
import json
import os

competitions = ['Serie_A', 'Serie_B']#, 'Serie_C', 'Serie_D', 'CdB']
players = {}
max_games = 0
for competition in competitions:
    for year in range(2022, 2017, -1):
        with open(f'../../Scrape/results/{competition}/{year}/squads.json', 'r') as f:
            squads = json.load(f)

        for game in squads:
            for substituition in squads[game]:
                for player in squads[game][substituition]['Mandante']:
                    if player not in players:
                        players[player] = 1
                    else:
                        players[player] += 1
                    
                    if players[player] > max_games:
                       max_games = players[player]
                
                for player in squads[game][substituition]['Visitante']:
                    if player not in players:
                        players[player] = 1
                    else:
                        players[player] += 1
                    
                    if players[player] > max_games:
                        max_games = players[player]

cont = {n : 0 for n in range(1, max_games + 1)}
for player in players:
    cont[players[player]] += 1
    
plt.bar(cont.keys(), cont.values())
plt.title('Número de subpartidas x Quantidade de jogadores')
plt.xlabel('Número de subpartidas')
plt.ylabel('Número de jogadores')
plt.savefig('games_played_per_player.png')
plt.show()

players_1 = 0
players_2 = 0
threshold = 20
for k in cont:
    players_1 += cont[k]
    if k < threshold and cont[k] > 0:
        players_2 += 1
    else:
        players_2 += cont[k]
        
print(players_1, players_2, players_2 / players_1)
