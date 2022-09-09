from numpy.random import poisson as rv_poisson
from numpy.random import multivariate_normal
from scipy.optimize import minimize
from scipy.stats import poisson
from glob import glob

import os
import json
import numpy as np
import matplotlib.pyplot as plt

def bivariate_poisson(lamb_1 = 1, lamb_2 = 1, lamb_3 = 0, size = 1):
    X_1 = rv_poisson(lamb_1, size)
    X_2 = rv_poisson(lamb_2, size)
    X_3 = rv_poisson(lamb_3, size)
    Y_1 = X_1 + X_3
    Y_2 = X_2 + X_3
    
    return np.vstack([Y_1, Y_2]).T

def is_positive_semidefinite(x, y, z):
    t1 = x + z - (x**2 - 2 * x * z + 4 * y**2 + z**2)**(1/2) >= 0
    t2 = x + z + (x**2 - 2 * x * z + 4 * y**2 + z**2)**(1/2) >= 0
    
    return t1 * t2

def games_probs(lamb_1 = 1, lamb_2 = 1, lamb_3 = 0, size = 100000):
    sims = bivariate_poisson(lamb_1, lamb_2, lamb_3, size)
    w = round(sum(np.greater(sims[:, 0], sims[:, 1])) / size, 4)
    l = round(sum(np.less(sims[:, 0], sims[:, 1])) / size, 4)
    d = round(1 - w - l, 4)

    return w, d, l
    
def games_results(lamb_1 = 1, lamb_2 = 1, lamb_3 = 0, size = 100000):
    sims = bivariate_poisson(lamb_1, lamb_2, lamb_3, size)
    R = np.zeros(np.max(sims, 0) + 1)
    for sim in sims:
        R[sim[0], sim[1]] += 1
    
    R = R / size
    w = round(np.sum(np.tril(R, -1)), 6)
    d = round(np.sum(np.diag(R)), 6)
    l = round(np.sum(np.triu(R, 1)), 6)
    
    return R, (w, d, l)

def game_likelihood(lambs, goals):
    lik_score_1 = poisson.logcdf(goals[0], lambs[0])
    lik_score_2 = poisson.logcdf(goals[1], lambs[1])
    
    return lik_score_1 + lik_score_2

def likelihood(proficiencies, players, squads):
    if proficiencies.shape[0] != len(players):
        proficiencies = proficiencies.reshape(len(players), 2)
    
    lik = 0
    for game in squads:
        for sub in squads[game]:
            lamb_11, lamb_12 = 0, 0
            lamb_21, lamb_22 = 0, 0
            goals = squads[game][sub]['Placar']
            t = squads[game][sub]['Tempo']
            if t != 0:
                for i in range(11):
                    player = squads[game][sub]['Mandante'][i]
                    lamb_11 += proficiencies[players[player], 0]
                    lamb_12 += proficiencies[players[player], 1]
                
                    player = squads[game][sub]['Visitante'][i]
                    lamb_21 += proficiencies[players[player], 0]
                    lamb_22 += proficiencies[players[player], 1]
            
                lamb_11 *= t / 90
                lamb_12 *= t / 90
                lamb_21 *= t / 90
                lamb_22 *= t / 90
                lambs = [lamb_11 / lamb_22, lamb_21 / lamb_12]
                lik += game_likelihood(lambs, goals)
            
    return - lik

with open('../../Scrape/Serie_A/2022/squads.json', 'r') as f:
    squads = json.load(f)
    
i = 0
players = {}
for game in squads:
    for sub in squads[game]:
        for player in squads[game][sub]['Mandante']:
            if player not in players:
                players[player] = i
                i += 1
                
        for player in squads[game][sub]['Visitante']:
            if player not in players:
                players[player] = i
                i += 1

mu1, mu2 = 1, 2
x, y, z = 2, 1, 2
proficiencies = np.abs(multivariate_normal([mu1, mu2], [[x, y], [y, z]], i)).reshape(2 * len(players), 1)
print(likelihood(proficiencies, players, squads))
res = minimize(likelihood, proficiencies, args = (players, squads))
print(res.fun)
print(res.nit)

#n = 1000000
# probs = games_probs(lamb_1 = 2, lamb_2 = 1, lamb_3 = 0, size = n)
#results, probs = games_results(lamb_1 = 2, lamb_2 = 1, lamb_3 = 0, size = n)

#print(probs)
#print(game_likelihood([2, 1], [3, 2]))
#print(game_likelihood([3, 2], [3, 2]))

