import os
import sys
import stan
import json
import shutil
import numpy as np
import httpstan.cache
import httpstan.models

from time import time
from datetime import datetime

def clean_cache(model):
    model_name = httpstan.models.calculate_model_name(model)
    httpstan.cache.delete_model_directory(model_name)

def collect_data(competitions, years, players_file):
    with open(players_file, 'r') as f:
        players = json.load(f)
    
    n_obs = 0
    n_players = len(players)
    times = []
    n_players_per_game = 11
    results = []
    club_1 = []
    club_2 = []
    for competition in competitions:
        for year in years:
            with open(f'../../../../Scrape/results/{competition}/{year}/squads.json', 'r') as f:
                squads = json.load(f)

            for game in squads:
                for substituition in squads[game]:
                    if squads[game][substituition]['Tempo'] == 0:
                        continue
                
                    n_obs += 1
                    times.append(squads[game][substituition]['Tempo'])
                    club_1.append([])
                    club_2.append([])
                    results.append(squads[game][substituition]['Placar'])
                    for player in squads[game][substituition]['Mandante']:
                        club_1[-1].append(players[player])
            
                    for player in squads[game][substituition]['Visitante']:
                        club_2[-1].append(players[player])

    assert len(club_1) == len(club_2)
    assert len(club_1) == len(results)
    assert len(club_1) == len(times)
    assert len(club_1) == n_obs
    data = {'n_obs': n_obs,
            'n_players': n_players,
            'times': times,
            'n_players_per_game': n_players_per_game,
            'results': results,
            'club_1': club_1,
            'club_2': club_2}

    return data, players

def run(model, data, chain, name, num_samples = 1000, num_warmup = 1000, clear_cache = True):
    if clear_cache:
        clean_cache(model)
    
    posterior = stan.build(model, data = data, random_seed = chain)
    fit = posterior.sample(num_chains = 1, num_samples = num_samples, num_warmup = num_warmup)
    df = fit.to_frame()
    df[:len(df) // 4].to_parquet(f'{name}_chain_{chain}_part_1.parquet')
    df[len(df) // 4:len(df) // 2].to_parquet(f'{name}_chain_{chain}_part_2.parquet')
    df[len(df) // 2:3 * len(df) // 4].to_parquet(f'{name}_chain_{chain}_part_3.parquet')
    df[3 * len(df) // 4:].to_parquet(f'{name}_chain_{chain}_part_4.parquet')

if __name__ == '__main__':
    start_time = time()
    model_name = 'HAM1'
    write_log = True
    if write_log:
        with open(f'../logs/{model_name}.log', 'a') as f:
            f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [Fitting - AD Model] - Iniciando recálculo dos parâmetros.\n')
    
    with open('../../../Scrape/auxiliary/scrape.log', 'r') as f:
        log = f.readlines()
        
    recalcular = log[-9].split() != []
    if not recalcular:
        if write_log:
            with open(f'../logs/{model_name}.log', 'a') as f:
                f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [Fitting - AD Model] - Parâmetros já atualizados.\n\n')
        
    else:
        os.chdir('../results/HAM1')
        model = '''
                  data {
                    int<lower = 1> n_obs;
                    int<lower = 1> n_players;
                    array[n_obs] int<lower = 1> times;
                    int<lower = 1> n_players_per_game;
                    array[n_obs, 2] int results;
                    array[n_obs, n_players_per_game] int club_1;
                    array[n_obs, n_players_per_game] int club_2;
                  }

                  parameters {
                    array[n_players] real<lower = 0> theta_atk_m;
                    array[n_players] real<lower = 0> theta_def_m;
                    array[n_players] real<lower = 0> theta_atk_v;
                    array[n_players] real<lower = 0> theta_def_v;
                  }

                  model {
                    theta_atk_m ~ std_normal();
                    theta_def_m ~ std_normal();
                    theta_atk_v ~ std_normal();
                    theta_def_v ~ std_normal();
                    for (n in 1:n_obs){
                      results[n, 1] ~ poisson(sum(theta_atk_m[club_1[n, ]]) / sum(theta_def_v[club_2[n, ]]) * times[n]);
                      results[n, 2] ~ poisson(sum(theta_atk_v[club_2[n, ]]) / sum(theta_def_m[club_1[n, ]]) * times[n]);
                    }
                  }
                '''
        
        chain = sys.argv[-1]
        chain = chain.split('=')[-1]
        chain = int(chain)
        name = sys.argv[-2]
        name = name.split('=')[-1]
        base_year = name[:2]
        div = name[2:]
        competitions = ['Serie_A', 'Serie_B', 'Serie_C', 'Serie_D', 'CdB']
        if div != 'CdB':
            competitions = competitions[:competitions.index('Serie_' + div) + 1]
        
        years = range(int(base_year) + 2000, 2023)
        data, players = collect_data(competitions, years, f'../../../Commons/players_{base_year}{div}_all.json')
        run(model, data, chain, name, num_samples = 500, num_warmup = 500)
        shutil.rmtree('build', ignore_errors = True)
        os.chdir('../../scripts')
        end_time = time()
        print(f'Cálculos finalizados em {end_time - start_time:.2f} segundos!')
        if write_log:
            with open(f'../logs/{model_name}.log', 'a') as f:
                f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [Fitting - AD Model] - Finalizado recálculo dos parâmetros.\n\n')