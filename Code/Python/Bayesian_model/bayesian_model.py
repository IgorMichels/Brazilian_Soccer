import stan
import json
import httpstan.cache
import httpstan.models

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
            with open(f'../../../Scrape/{competition}/{year}/squads.json', 'r') as f:
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

def run(model, data, n_iter, base_player, name, num_samples = 1000, num_warmup = 1000, clear_cache = True):
    for chain in range(1, n_iter + 1):
        if clear_cache:
            clean_cache(model)
        
        posterior = stan.build(model, data = data, random_seed = chain)
        fit = posterior.sample(num_chains = 1, num_samples = num_samples, num_warmup = num_warmup)
        df = fit.to_frame()
        
        for column in df.columns[7:]:
            df[column] = df[column] / df.loc[0, f'theta_1.{base_player}']
            
        df[:len(df) // 2].to_csv(f'{name}_part_1.csv')
        df[len(df) // 2:].to_csv(f'{name}_part_2.csv')

if __name__ == '__main__':
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
                array[n_players] real<lower = 0> theta_1;
                array[n_players] real<lower = 0> theta_2;
              }

              model {
                theta_1 ~ std_normal();
                theta_2 ~ std_normal();
                for (n in 1:n_obs){
                  results[n, 1] ~ poisson(sum(theta_1[club_1[n, ]]) / sum(theta_2[club_2[n, ]]) * times[n]);
                  results[n, 2] ~ poisson(sum(theta_1[club_2[n, ]]) / sum(theta_2[club_1[n, ]]) * times[n]);
                }
              }
            '''
    
    competitions = ['Serie_A', 'Serie_B']
    for base_year in range(2013, 2022):
        years = range(base_year, 2022)
        data, players = collect_data(competitions, years, f'../Commons/players_{str(years[0])[-2:]}{competitions[-1][-1]}_all.json')
        base_player = '502361'
        base_player = players[base_player]
        n_iter = 1
        name = f'parameters_std_normal_prior_{str(years[0])[-2:]}{competitions[-1][-1]}'
        run(model, data, n_iter, base_player, name, num_samples = 1000)
