import json
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import poisson, chi2

if __name__ == '__main__':
    home = []
    away = []
    competitions = ['Serie_A', 'Serie_B']
    years = range(2013, 2022)
    for competition in competitions:
        for year in years:
            opening = f'../../../Scrape/{competition}/{year}/squads.json'
            with open(opening, 'r') as f:
                squads = json.load(f)
    
            for game in squads:
                home_score, away_score = 0, 0
                for sub in squads[game]:
                    home_score += squads[game][sub]['Placar'][0]
                    away_score += squads[game][sub]['Placar'][1]
                
                home.append(home_score)
                away.append(away_score)
    
    home_avg = np.mean(home)
    away_avg = np.mean(away)
    home_std = np.std(home)
    away_std = np.std(away)
    
    home, home_counts = np.unique(home, return_counts = True)
    away, away_counts = np.unique(away, return_counts = True)
    
    home_pois = poisson.pmf(home, mu = home_avg)
    away_pois = poisson.pmf(away, mu = away_avg)
    expected_home = home_pois * np.sum(home_counts)
    expected_away = away_pois * np.sum(away_counts)
    
    print(round(np.sum((home_counts - expected_home)**2 / expected_home), 4), round(chi2.isf(0.05, len(home) - 2), 4))
    print(round(np.sum((away_counts - expected_away)**2 / expected_away), 4), round(chi2.isf(0.05, len(away) - 2), 4))
    
    home_counts = home_counts / np.sum(home_counts)
    away_counts = away_counts / np.sum(away_counts)
    plt.bar(home, home_counts * 100, label = 'Gols - mandante', alpha = 0.7)
    plt.bar(away, away_counts * 100, label = 'Gols - visitante', alpha = 0.7)
    plt.plot(home, home_pois * 100, label = f'Poisson({home_avg:.2f})')
    plt.plot(away, away_pois * 100, label = f'Poisson({away_avg:.2f})')
    plt.legend()
    plt.xlabel('Gols')
    plt.ylabel('Jogos (%)')
    plt.title(f'Gols por partida\nSéries A e B ({years[0]} - {years[-1]})')
    plt.savefig('goals.png')
    plt.show()
