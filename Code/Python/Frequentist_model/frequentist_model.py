from scipy.optimize import minimize, LinearConstraint
from numpy.random import poisson as rv_poisson
from numpy.random import multivariate_normal
from scipy.stats import poisson
from math import factorial
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
    lik_score_1 = poisson.logpmf(goals[0], lambs[0])
    lik_score_2 = poisson.logpmf(goals[1], lambs[1])
    
    return lik_score_1 + lik_score_2

def likelihood(proficiencies, players, squads):
    n = len(players)
    lik_1, lik_2 = 0, 0
    for game in squads:
        for sub in squads[game]:
            lamb_ma, lamb_md, lamb_va, lamb_vd = 0, 0, 0, 0
            goals = squads[game][sub]['Placar']
            t = squads[game][sub]['Tempo']
            if t != 0:
                for i in range(11):
                    player = squads[game][sub]['Mandante'][i]
                    lamb_ma += proficiencies[players[player]]
                    lamb_md += proficiencies[players[player] + n]
                
                    player = squads[game][sub]['Visitante'][i]
                    lamb_va += proficiencies[players[player]]
                    lamb_vd += proficiencies[players[player] + n]
            
                lamb_1 = lamb_ma / lamb_vd * t
                lamb_2 = lamb_va / lamb_md * t
                if lamb_1 <= 0 or lamb_2 <= 0: return np.inf
                lambs = [lamb_1, lamb_2]
                lik_1 += game_likelihood(lambs, goals)
                lik_2 += - lamb_1 + goals[0] * np.log(lamb_1) - np.log(factorial(goals[0]))
                lik_2 += - lamb_2 + goals[1] * np.log(lamb_2) - np.log(factorial(goals[1]))
                
    return lik_1

def likelihood_gradient(proficiencies, players, squads):
    n = len(players)
    gradient = np.zeros(2 * n)
    for game in squads:
        for sub in squads[game]:
            lamb_ma, lamb_md, lamb_va, lamb_vd = 0, 0, 0, 0
            s_m, s_v = squads[game][sub]['Placar']
            t = squads[game][sub]['Tempo']
            if t != 0:
                for i in range(11):
                    player = players[squads[game][sub]['Mandante'][i]]
                    lamb_ma += proficiencies[player    ]
                    lamb_md += proficiencies[player + n]
                
                    player = players[squads[game][sub]['Visitante'][i]]
                    lamb_va += proficiencies[player    ]
                    lamb_vd += proficiencies[player + n]
            
                for i in range(11):
                    player = players[squads[game][sub]['Mandante'][i]]
                    gradient[player    ] += - t / lamb_vd + s_m / lamb_ma
                    gradient[player + n] += t / lamb_md * lamb_va / lamb_md - s_v / lamb_md
                    
                    player = players[squads[game][sub]['Visitante'][i]]
                    gradient[player    ] += - t / lamb_md + s_v / lamb_va
                    gradient[player + n] += t / lamb_vd * lamb_ma / lamb_vd - s_m / lamb_vd
                
    return gradient

def likelihood_hessian(proficiencies, players, squads):
    n = len(players)
    hessian = np.zeros((2 * n, 2 * n))
    for game in squads:
        for sub in squads[game]:
            lamb_ma, lamb_md, lamb_va, lamb_vd = 0, 0, 0, 0
            s_m, s_v = squads[game][sub]['Placar']
            t = squads[game][sub]['Tempo']
            if t != 0:
                for i in range(11):
                    player = players[squads[game][sub]['Mandante'][i]]
                    lamb_ma += proficiencies[player    ]
                    lamb_md += proficiencies[player + n]
                
                    player = players[squads[game][sub]['Visitante'][i]]
                    lamb_va += proficiencies[player    ]
                    lamb_vd += proficiencies[player + n]
            
                for i in range(11):
                    player_i = players[squads[game][sub]['Mandante'][i]]
                    for j in range(11):
                        player_j = players[squads[game][sub]['Mandante'][j]]
                        hessian[player_i    , player_j    ] += - s_m / (lamb_ma ** 2) # atk/atk
                        hessian[player_i    , player_j + n] += 0 # atk/def
                        hessian[player_i + n, player_j    ] += 0 # def/atk
                        hessian[player_i + n, player_j + n] += s_v / (lamb_md ** 2) - 2 * t * lamb_va / (lamb_md ** 3) # def/def
                        
                        player_j = players[squads[game][sub]['Visitante'][j]]
                        hessian[player_i    , player_j    ] += 0 # atk/atk
                        hessian[player_i    , player_j + n] += t / (lamb_vd ** 2) # atk/def
                        hessian[player_i + n, player_j    ] += t / (lamb_md ** 2) # def/atk
                        hessian[player_i + n, player_j + n] += 0 # def/def
                        
                    player_i = players[squads[game][sub]['Visitante'][i]]
                    for j in range(11):
                        player_j = players[squads[game][sub]['Mandante'][j]]
                        hessian[player_i    , player_j    ] += 0 # atk/atk
                        hessian[player_i    , player_j + n] += t / (lamb_md ** 2) # atk/def
                        hessian[player_i + n, player_j    ] += t / (lamb_vd ** 2) # def/atk
                        hessian[player_i + n, player_j + n] += 0 # def/def
                        
                        player_j = players[squads[game][sub]['Visitante'][j]]
                        hessian[player_i    , player_j    ] += - s_v / (lamb_va ** 2) # atk/atk
                        hessian[player_i    , player_j + n] += 0 # atk/def
                        hessian[player_i + n, player_j    ] += 0 # def/atk
                        hessian[player_i + n, player_j + n] += s_m / (lamb_vd ** 2) - 2 * t * lamb_ma / (lamb_vd ** 3) # def/def
                        
    return hessian

with open('../../../Scrape/Serie_A/2021/squads.json', 'r') as f:
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

mu = 0
sigma = 3
proficiencies = np.abs(np.random.normal(mu, sigma, 2 * len(players)))
# menor, maior = 1e-20, 1e20
# bounds = [(menor, maior) for i in range(len(proficiencies))]
# bounds[0] = (1, 1)
proficiencies[0] = 1
res = minimize(likelihood,
               proficiencies,
               args = (players, squads),
               method = 'Newton-CG',
               jac = likelihood_gradient,
               hess = likelihood_hessian,
               # bounds = bounds,
               tol = 1e-6
              )

np.save('result_hessian.npy', res.x)
print(res.x)
print(res.fun)

# n = 1000000
# probs = games_probs(lamb_1 = 2, lamb_2 = 1, lamb_3 = 0, size = n)
# results, probs = games_results(lamb_1 = 2, lamb_2 = 1, lamb_3 = 0, size = n)

# print(probs)
# print(game_likelihood([2, 1], [3, 2]))
# print(game_likelihood([3, 2], [3, 2]))

