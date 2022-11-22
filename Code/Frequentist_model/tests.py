from numpy.random import random

import matplotlib.pyplot as plt
import numpy as np
import json

max_year = 2022
competitions = ['CdB',
                'Serie_A',
                'Serie_B',
                'Serie_C',
                'Serie_D'
                ]

cod = 0
players = {}
sub_games = 0
players_ids = {}
for competition in competitions:
    for year in range(2013, max_year + 1):
        with open(f'../../Scrape/results/{competition}/{year}/squads.json', 'r') as f:
            squads = json.load(f)
            
        for game in squads:
            for substituition in squads[game]:
                sub_games += 1
                for player in squads[game][substituition]['Mandante']:
                    if player not in players:
                        players[player] = squads[game][substituition]['Tempo']
                        players_ids[player] = cod
                        cod += 1
                    else:
                        players[player] += squads[game][substituition]['Tempo']
                
                for player in squads[game][substituition]['Visitante']:
                    if player not in players:
                        players[player] = squads[game][substituition]['Tempo']
                        players_ids[player] = cod
                        cod += 1
                    else:
                        players[player] += squads[game][substituition]['Tempo']

times = {}
for player in players:
    if players[player] not in times:
        times[players[player]] = [player]
    else:
        times[players[player]].append(player)
        
#print(max(times), max(times) / 90, times[max(times)])
#print(min(times), min(times) / 90, times[min(times)])
print(len(players), sub_games)

'''
x = []
y = []
for time in times:
    x.append([time, len(times[time])])

x = sorted(x, key = lambda k : k[0])
x = np.array(x)
plt.plot(x[:, 0], x[:, 1])
plt.show()
'''

p = random((len(players), 2))
#print((p.reshape((2 * len(players), 1)).reshape((len(players), 2)) == p).all())
#print(players_ids)

print(squads)



