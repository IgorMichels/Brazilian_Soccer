'''
Algoritmo ELO original
'''

# import's
import numpy as np
import pandas as pd
from copy import copy

# criando dados falsos
forcas = list(np.floor(np.random.normal(1200, 100, 20)))
jogos = np.zeros((380, 4), int) # home, score home, score away, away
ordem = pd.read_csv('ordem.csv')
jogos[:, 0] = np.hstack([ordem['h'].values - 1, ordem['a'].values - 1])
jogos[:, 3] = np.hstack([ordem['a'].values - 1, ordem['h'].values - 1])
jogos = np.vstack([jogos for i in range(10)])
for i in range(len(jogos)):
	jogos[i, 1] = np.random.poisson(forcas[jogos[i, 0]] / forcas[jogos[i, 3]])
	jogos[i, 2] = np.random.poisson(forcas[jogos[i, 3]] / forcas[jogos[i, 0]])

# implementando o ELO
def score_esperado(RA, RB):
	return (1 + 10 ** ((RA - RB) / 400)) ** (-1)

def atualiza_rating(RA, RB, SA, SB, KA, KB):
	EA = score_esperado(RA, RB)
	EB = 1 - EA
	CA = (SA - EA) * KA
	CB = (SB - EB) * KB
	RA = RA + CA
	RB = RB + CB
	
	return RA, RB

def ELO(jogos, forcas, Ki = 40, Kn = 25, filtro = 7):
	n_jogos = len(jogos)
	n_clubes = len(forcas)
	jogados = [0 for i in range(n_clubes)]
	for i in range(n_jogos):
		cA, sA, sB, cB = jogos[i, :]
		if sA > sB:
			SA = 1
		elif sA == sB:
			SA = 0.5
		else:
			SA = 0
			
		SB = 1 - SA
		
		if jogados[cA] < filtro:
			KA = Ki
		else:
			KA = Kn
			
		if jogados[cB] < filtro:
			KB = Ki
		else:
			KB = Kn
		
		RA, RB = forcas[cA], forcas[cB]
		RA, RB = atualiza_rating(RA, RB, SA, SB, KA, KB)
		forcas[cA], forcas[cB] = RA, RB
	
	return forcas

novas_forcas = ELO(jogos, copy(forcas))
print(forcas)
print(novas_forcas)
