import json

def create_clubs(years, competitions):
    clubs = {}
    n_clubs = 1
    for competition in competitions:
        for year in years:
            with open(f'../../Scrape/results/{competition}/{year}/games.json', 'r') as f:
                games = json.load(f)
                
            for game in games:
                club = games[game]['Mandante']
                if club not in clubs:
                    clubs[club] = n_clubs
                    n_clubs += 1
                    
    return clubs

def sum_players_times(years, competitions):
    players_time = {}
    players_subgames = {}
    for competition in competitions:
        for year in years:
            with open(f'../../Scrape/results/{competition}/{year}/squads.json', 'r') as f:
                squads = json.load(f)

            for game in squads:
                for substituition in squads[game]:
                    if squads[game][substituition]['Tempo'] == 0:
                        continue
                
                    time = squads[game][substituition]['Tempo']
                    for player in squads[game][substituition]['Mandante']:
                        if player not in players_time:
                            players_time[player] = time
                            players_subgames[player] = 1
                        else:
                            players_time[player] += time
                            players_subgames[player] += 1
                        
                    for player in squads[game][substituition]['Visitante']:
                        if player not in players_time:
                            players_time[player] = time
                            players_subgames[player] = 1
                        else:
                            players_time[player] += time
                            players_subgames[player] += 1

    return players_time, players_subgames

def create_clustered_players(years, competitions, time = False, params = {'k' : 10, 'min_time' : 600, 'interval' : 15}):
    if time:
        players, _ = sum_players_times(years, competitions)
        min_time, interval = params['min_time'], params['interval']
        n = (min_time - 1) // interval + 1
        for player in players:
            if players[player] < min_time:
                players[player] = players[player] // interval + 1
            else:
                players[player] = n
                n += 1
    else:
        _, players = sum_players_times(years, competitions)
        k = params['k']
        n = k
        for player in players:
            if players[player] >= k:
                players[player] = n
                n += 1
    
    return players

def create_players(years, competitions):
    return create_clustered_players(years, competitions, time = False, params = {'k' : 1})

if __name__ == '__main__':
    competitions = ['Serie_A', 'Serie_B']
    years = range(2013, 2023)
    for base_year in years:
        new_years = range(base_year, 2023)
        players = create_players(new_years, competitions)
        print(f'players_{str(new_years[0])[-2:]}{competitions[-1][-1]}_all.json')
        with open(f'players_{str(new_years[0])[-2:]}{competitions[-1][-1]}_all.json', 'w') as f:
            json.dump(players, f)
            
        clubs = create_clubs(years, competitions)
        print(f'clubs_{str(new_years[0])[-2:]}{competitions[-1][-1]}.json')
        with open(f'clubs_{str(new_years[0])[-2:]}{competitions[-1][-1]}.json', 'w') as f:
            json.dump(clubs, f)
