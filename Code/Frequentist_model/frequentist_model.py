import json
import numpy as np

from copy import deepcopy
from scipy.stats import poisson
from numpy.linalg import norm
from scipy.optimize import minimize, fmin

def calculate_lambs(subgame, players, proficiencies):
    n = len(players)
    lamb_ma, lamb_md, lamb_va, lamb_vd = 0, 0, 0, 0
    for i in range(11):
        player = players[subgame['Mandante'][i]]
        lamb_ma += proficiencies[player    ]
        lamb_md += proficiencies[player + n]
        
        player = players[subgame['Visitante'][i]]
        lamb_va += proficiencies[player    ]
        lamb_vd += proficiencies[player + n]
    
    return lamb_ma, lamb_md, lamb_va, lamb_vd

def game_likelihood(lambs, goals):
    lik_score_1 = poisson.logpmf(goals[0], lambs[0])
    lik_score_2 = poisson.logpmf(goals[1], lambs[1])
    
    return lik_score_1 + lik_score_2

def likelihood(proficiencies, players, squads):
    if any(proficiencies <= 0): return np.inf
    n = len(players)
    lik = 0
    for game in squads:
        for sub in squads[game]:
            lamb_ma, lamb_md, lamb_va, lamb_vd = 0, 0, 0, 0
            goals = squads[game][sub]['Placar']
            t = squads[game][sub]['Tempo']
            if t != 0:
                lamb_ma, lamb_md, lamb_va, lamb_vd = calculate_lambs(squads[game][sub],
                                                                     players,
                                                                     proficiencies)
            
                lamb_1 = lamb_ma / lamb_vd * t
                lamb_2 = lamb_va / lamb_md * t
                if lamb_1 <= 0 or lamb_2 <= 0: return np.inf
                lambs = [lamb_1, lamb_2]
                lik += game_likelihood(lambs, goals)
                
    return - lik

def likelihood_gradient(proficiencies, players, squads):
    n = len(players)
    gradient = np.zeros(2 * n)
    for game in squads:
        for sub in squads[game]:
            s_m, s_v = squads[game][sub]['Placar']
            t = squads[game][sub]['Tempo']
            if t != 0:
                lamb_ma, lamb_md, lamb_va, lamb_vd = calculate_lambs(squads[game][sub],
                                                                     players,
                                                                     proficiencies)
                
                for i in range(11):
                    player = players[squads[game][sub]['Mandante'][i]]
                    gradient[player    ] += - t / lamb_vd + s_m / lamb_ma
                    gradient[player + n] += t / lamb_md * lamb_va / lamb_md - s_v / lamb_md
                    
                    player = players[squads[game][sub]['Visitante'][i]]
                    gradient[player    ] += - t / lamb_md + s_v / lamb_va
                    gradient[player + n] += t / lamb_vd * lamb_ma / lamb_vd - s_m / lamb_vd
                
    return - gradient

def likelihood_hessian(proficiencies, players, squads):
    n = len(players)
    hessian = np.zeros((2 * n, 2 * n))
    for game in squads:
        for sub in squads[game]:
            s_m, s_v = squads[game][sub]['Placar']
            t = squads[game][sub]['Tempo']
            if t != 0:
                lamb_ma, lamb_md, lamb_va, lamb_vd = calculate_lambs(squads[game][sub],
                                                                     players,
                                                                     proficiencies)
                
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
                        
    return - hessian

def collect_data(years, competitions, players_file):
    with open(players_file, 'r') as f:
        players = json.load(f)
    
    for player in players:
        players[player] -= 1
    
    game_id = 0
    new_squads = {}
    for competition in competitions:
        for year in years:
            with open(f'../../Scrape/{competition}/{year}/squads.json', 'r') as f:
                squads = json.load(f)
            
            for game in squads:
                game_id += 1
                new_squads[str(game_id).zfill(5)] = deepcopy(squads[game])
                #for sub in squads[game]:
                #    if squads[game][sub]['Tempo'] != 0:
                #        new_squads[str(game_id).zfill(5)][sub]['Mandante'] = []
                #        for player in squads[game][sub]['Mandante']:
                #            new_squads[str(game_id).zfill(5)][sub]['Mandante'].append(players[player])
                #    
                #        new_squads[str(game_id).zfill(5)][sub]['Visitante'] = []
                #        for player in squads[game][sub]['Visitante']:
                #            new_squads[str(game_id).zfill(5)][sub]['Visitante'].append(players[player])
                    
    return players, new_squads

def optimizer(proficiencies, players, squads, max_iter = 10000, eps = 1e-6, tol = 1e-8):
    fx_ant = np.inf
    fx = likelihood(proficiencies, players, squads)
    gx = likelihood_gradient(proficiencies, players, squads)
    n_iter = 0
    while n_iter < max_iter and norm(gx) > eps and abs(fx_ant - fx) > tol:
        n_iter += 1
        t = 1
        while fx < likelihood(proficiencies - t * gx, players, squads):
            t = t / 1.5
            
        proficiencies -= t * gx
        fx_ant = fx
        fx = likelihood(proficiencies, players, squads)
        gx = likelihood_gradient(proficiencies, players, squads)
        print(n_iter, fx, norm(gx), t)
        
    return proficiencies, n_iter, fx, gx

if __name__ == '__main__':
    competitions = ['Serie_A', 'Serie_B']
    years = [2022]#range(2018, 2023)
    players_file = f'../Commons/players_{str(years[0])[-2:]}{competitions[-1][-1]}_20_games.json'
    players, squads = collect_data(years, competitions, players_file)
    mu = 0
    sigma = 3
    proficiencies = np.abs(np.random.normal(mu, sigma, 2 * len(players)))
    proficiencies[0] = 1
    #res = minimize(
    #               likelihood,
    #               proficiencies,
    #               args = (players, squads),
    #               # method = 'trust-exact',
    #               # method = 'Newton-CG',
    #               jac = likelihood_gradient,
    #               hess = likelihood_hessian,
    #               tol = 1e-6,
    #               #options = {
    #               #           'xtol': 1e-20,
    #               #           'eps' : 1e-10
    #               #          }
    #              )
                  
    res = fmin(
               likelihood,
               proficiencies,
               args = (players, squads),
              )

    np.save('result_fmin.npy', res.x)
    #np.save('result_trust_exact.npy', res.x)
    #np.save('newton_cg.npy', res.x)
    print(proficiencies)
    print(res.x)
    print(res.fun)
    print(res)
    
    #proficiencies_opt, n_iter, fx, gx = optimizer(deepcopy(proficiencies), players, squads, max_iter = 10000, eps = 1e-6)
    #proficiencies_opt = proficiencies_opt / proficiencies_opt[0]
    #print()
    #print(norm(proficiencies - proficiencies_opt))
    #print(proficiencies)
    #print(proficiencies_opt)
