import stan
import json
import numpy as np
import httpstan.cache
import httpstan.models

def clean_cache(model):
    model_name = httpstan.models.calculate_model_name(model)
    httpstan.cache.delete_model_directory(model_name)

def collect_data(competitions, years):
    with open(f'../Commons/players_{str(years[0])[-2:]}{competitions[-1][-1]}_all.json', 'r') as f:
        players = json.load(f)
    
    with open(f'../Commons/clubs_{str(years[0])[-2:]}{competitions[-1][-1]}.json', 'r') as f:
        clubs = json.load(f)
    
    n_obs = 0
    n_players = len(players)
    times = []
    n_players_per_game = 11
    results = []
    club_1 = []
    club_2 = []
    home_clubs = []
    for competition in competitions:
        for year in years:
            with open(f'../../Scrape/{competition}/{year}/squads.json', 'r') as f:
                squads = json.load(f)
                
            with open(f'../../Scrape/{competition}/{year}/games.json', 'r') as f:
                games = json.load(f)

            for game in squads:
                home_club = games[game]['Mandante']
                for substituition in squads[game]:
                    if squads[game][substituition]['Tempo'] == 0:
                        continue
                
                    n_obs += 1
                    home_clubs.append(clubs[home_club])
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
    assert len(club_1) == len(home_clubs)
    assert len(club_1) == n_obs
    data = {'n_obs': n_obs,
            'n_clubs' : len(home_clubs),
            'n_players': n_players,
            'n_players_per_game': n_players_per_game,
            'times': times,
            'home_clubs' : home_clubs,
            'results': results,
            'club_1': club_1,
            'club_2': club_2}

    return data, players, clubs

def run(model, data, n_iter, base_player, name, num_samples = 1000, num_warmup = 1000, clear_cache = True):
    for chain in range(1, n_iter + 1):
        if clear_cache:
            clean_cache(model)
        
        posterior = stan.build(model, data = data, random_seed = chain)
        fit = posterior.sample(num_chains = 1, num_samples = num_samples, num_warmup = num_warmup)
        df = fit.to_frame()
        avg = np.mean(df[f'theta_atk.{base_player}'])
        #for column in df.columns[7:]:
        #    df[column] = df[column] / avg
            
        df[:len(df) // 4].to_parquet(f'{name}_chain_{chain}_part_1.parquet')
        df[len(df) // 4:len(df) // 2].to_parquet(f'{name}_chain_{chain}_part_2.parquet')
        df[len(df) // 2:3 * len(df) // 4].to_parquet(f'{name}_chain_{chain}_part_3.parquet')
        df[3 * len(df) // 4:].to_parquet(f'{name}_chain_{chain}_part_4.parquet')

if __name__ == '__main__':
    model = '''
              data {
                int n_obs;
                int n_clubs;
                int n_players;
                int n_players_per_game;
                array[n_obs] int times;
                array[n_obs] int home_clubs;
                array[n_obs, 2] int results;
                array[n_obs, n_players_per_game] int club_1;
                array[n_obs, n_players_per_game] int club_2;
              }

              parameters {
                array[n_players] real<lower = 0> theta_atk;
                array[n_players] real<lower = 0> theta_def;
                array[n_clubs] real<lower = 0> sigma;
              }

              model {
                theta_atk ~ std_normal();
                theta_def ~ std_normal();
                sigma ~ std_normal();
                for (n in 1:n_obs){
                  results[n, 1] ~ poisson((sum(theta_atk[club_1[n, ]]) / sum(theta_def[club_2[n, ]]) + sigma[home_clubs[n]]) * times[n]);
                  results[n, 2] ~ poisson(sum(theta_atk[club_2[n, ]]) / sum(theta_def[club_1[n, ]]) * times[n]);
                }
              }
            '''
    
    competitions = ['Serie_A', 'Serie_B']
    for base_year in range(2022, 2012, -1):
        years = range(base_year, 2023)
        data, players, clubs = collect_data(competitions, years)
        base_player = '691654' # german cano
        base_player = players[base_player]
        n_iter = 2
        name = f'home_away_model_2/parameters_std_normal_prior_{str(years[0])[-2:]}{competitions[-1][-1]}_home_away_2'
        clean_cache(model)
        run(model, data, n_iter, base_player, name, num_samples = 500, num_warmup = 500)
