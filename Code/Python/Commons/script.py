import json

def sum_players_times(years, competitions):
    players_time = {}
    players_subgames = {}
    for competition in competitions:
        for year in years:
            with open(f'../../../Scrape/{competition}/{year}/squads.json', 'r') as f:
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
            if players[player] < k:
                players[player] -= 1
            else:
                players[player] = n
                n += 1
    
    return players

def create_players(years, competitions):
    return create_clustered_players(years, competitions, time = False, params = {'k' : 0})

if __name__ == '__main__':
    competitions = ['Serie_A', 'Serie_B']
    for base_year in range(2013, 2022):
        years = range(base_year, 2022)
        players = create_players(years, competitions)
        with open(f'players_{str(years[0])[:-2]}{competitions[-1][-1]}.json', 'w') as f:
            json.dump(players, f)
