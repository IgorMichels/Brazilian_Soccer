'''
Algoritmo ELO com mando de campo
'''

# import's
import numpy as np
import pandas as pd
import random as rd
from copy import copy, deepcopy

# criando dados falsos
anos = 10
jogadores = 20 * 18
jogadores = np.arange(jogadores, dtype = int)
equipes = {}
for ano in range(anos):
	rd.shuffle(jogadores)
	equipes[ano] = jogadores.reshape(20, 18).tolist()

aux = [np.floor(np.random.normal(1200, 100, 18)).tolist() for i in range(20)]
forcas = []
for item in aux:
	forcas += item

jogos = np.zeros((380, 4), int) # home, score home, score away, away
ordem = pd.read_csv('ordem.csv')
jogos[:, 0] = np.hstack([ordem['h'].values - 1, ordem['a'].values - 1])
jogos[:, 3] = np.hstack([ordem['a'].values - 1, ordem['h'].values - 1])
jogos = np.vstack([jogos for i in range(anos)])
escalacoes = {} # jogo : [casa [jogadores [indice, minutos]], fora [jogadores [indice, minutos]]]
for i in range(anos):
	for j in range(380):
		jogo = 380 * i + j
		index_time_A = jogos[jogo, 0]
		index_time_B = jogos[jogo, 3]
		time_A = deepcopy(equipes[ano][index_time_A])
		time_B = deepcopy(equipes[ano][index_time_B])
		rd.shuffle(time_A)
		rd.shuffle(time_B)
		n_jogadores_usados_A = rd.choice([11, 12, 13, 14])
		n_jogadores_usados_B = rd.choice([11, 12, 13, 14])
		forca_time_A = 0
		forca_time_B = 0
		for k in range(len(time_A)):
			if k + 11 < n_jogadores_usados_A:
				tempo = np.floor(np.random.normal(60, 10))
				time_A[k] = [time_A[k], tempo]
			elif k >= n_jogadores_usados_A:
				time_A[k] = [time_A[k], 0]
			elif 11 <= k < n_jogadores_usados_A:
				time_A[k] = [time_A[k], 90 - time_A[k - 11][1]]
			else:
				time_A[k] = [time_A[k], 90]
			
			if k + 11 < n_jogadores_usados_B:
				tempo = np.floor(np.random.normal(60, 10))
				time_B[k] = [time_B[k], tempo]
			elif k >= n_jogadores_usados_B:
				time_B[k] = [time_B[k], 0]
			elif 11 <= k < n_jogadores_usados_B:
				time_B[k] = [time_B[k], 90 - time_B[k - 11][1]]
			else:
				time_B[k] = [time_B[k], 90]
			
			forca_time_A += forcas[time_A[k][0]] * time_A[k][1]
			forca_time_B += forcas[time_B[k][0]] * time_B[k][1]
		
		escalacoes[jogo] = [time_A, time_B]
		jogos[jogo, 1] = np.random.poisson(forca_time_A / forca_time_B)
		jogos[jogo, 2] = np.random.poisson(forca_time_B / forca_time_A)

# implementando o ELO
def score_esperado(RA, RB, H):
	return (1 + 10 ** ((RA + H - RB) / 400)) ** (-1)

def atualiza_rating(RA, RB, SA, SB, KA, KB, H):
	EA = score_esperado(RA, RB, H)
	EB = 1 - EA
	CA = (SA - EA) * KA
	CB = (SB - EB) * KB
	RA = RA + CA
	RB = RB + CB
	H = H + CA
	
	return RA, RB, H

def ELO(jogos, forcas, Ki = 40, Kn = 25, filtro = 7, Hi = 120):
	n_jogos = len(jogos)
	n_clubes = len(forcas)
	jogados = [0 for i in range(n_clubes)]
	Hs = [Hi for i in range(n_clubes)]
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
		H = Hs[cA]
		RA, RB, H = atualiza_rating(RA, RB, SA, SB, KA, KB, H)
		forcas[cA], forcas[cB] = RA, RB
		Hs[cA] = H
	
	return forcas

novas_forcas = ELO(jogos, copy(forcas))
#print(forcas)
#print(novas_forcas)
