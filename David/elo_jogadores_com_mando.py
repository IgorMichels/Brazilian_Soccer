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
def score_esperado(escalacao_A, escalacao_B, H, forcas):
	tempo = 0
	RA = 0
	RB = 0
	for jogador in escalacao_A:
		tempo += jogador[1]
		RA += forcas[jogador[0]] * jogador[1]
		
	for jogador in escalacao_B:
		RB += forcas[jogador[0]] * jogador[1]
	
	RA = RA / tempo
	RB = RB / tempo
	return (1 + 10 ** ((RA + H - RB) / 400)) ** (-1)

def atualiza_rating(escalacao_A, escalacao_B, D, H, forcas, Ks, qs):
	'''
	SA     : float, score do time A
	SB     : float, score do time B
	D      : int, diferença no placar (gols A - gols B)
	H      : float, força do mando de campo
	forcas : vetor com as forças de cada jogador
	Ks     : vetor dos K's
	qs     : vetor dos q's
	'''
	impacto_cA = {}
	impacto_cB = {}
	if D > 0:
		SA = 1
	elif D == 0:
		SA = 0.5
	else:
		SA = 0
	
	SB = 1 - SA
	D = abs(D)
	EA = score_esperado(escalacao_A, escalacao_B, H, forcas)
	EB = 1 - EA
	C_time_A = 0
	C_time_B = 0
	tempo_total_A = 0
	tempo_total_B = 0
	for jogador in escalacao_A:
		t = jogador[1] / 90 # fixado M_max = 90
		if D == 0:
			C = (SA - EA) * t
		else:
			C = (SA - EA) * D ** (1 / 2)
		
		impacto_cA[jogador[0]] = [C, jogador[1]]
		K = Ks[jogador[0]]
		q = qs[jogador[0]]
		# a força muda mesmo que um jogador não entrou em campo
		# quando o time ganha ou perde
		forcas[jogador[0]] += K * (q * C + (1 - q) * C * t)
		if jogador[1] == 0:
			# o jogador não jogou
			Ks[jogador[0]] += 0.5
			qs[jogador[0]] += 0.025
		else:
			# ele jogou
			C_time_A += C
			tempo_total_A += jogador[1]
			Ks[jogador[0]] -= 0.25
			qs[jogador[0]] -= 0.025
	
	for jogador in escalacao_B:
		t = jogador[1] / 90 # fixado M_max = 90
		if D == 0:
			C = (SB - EB) * t
		else:
			C = (SB - EB) * D ** (1 / 2)
		
		impacto_cB[jogador[0]] = [C, jogador[1]]
		K = Ks[jogador[0]]
		q = qs[jogador[0]]
		# a força muda mesmo que um jogador não entrou em campo
		# quando o time ganha ou perde
		forcas[jogador[0]] += K * (q * C + (1 - q) * C * t)
		if jogador[1] == 0:
			# o jogador não jogou
			Ks[jogador[0]] += 0.5
			qs[jogador[0]] += 0.025
		else:
			# ele jogou
			C_time_B += C
			tempo_total_B += jogador[1]
			Ks[jogador[0]] -= 0.25
			qs[jogador[0]] -= 0.025
	
	H += C_time_A
	impacto_cA['C'] = C_time_A
	impacto_cA['tempo'] = tempo_total_A
	impacto_cB['C'] = C_time_B
	impacto_cB['tempo'] = tempo_total_B
	return forcas, Ks, qs, H, impacto_cA, impacto_cB

def ELO(jogos, forcas, escalacoes, Ks, qs, Hs, anos):
	impactos = {}
	for i in range(anos):
		for time in range(20):
			for jogador in equipes[i][time]:
				if i == 0:
					impactos[jogador] = {}
				else:
					if jogador not in equipes[i - 1][time]:
						# fazendo a correção dos parâmetros pela troca de clube
						Ks[jogador] = 40
						qs[jogador] = 1
						
		for j in range(380):
			jogo = i * 380 + j
			cA, sA, sB, cB = jogos[jogo, :]
			D = sA - sB
			H = Hs[cA]
			escalacao_A, escalacao_B = escalacoes[jogo]
			forcas, Ks, qs, H, impacto_cA, impacto_cB = atualiza_rating(escalacao_A, escalacao_B, D, H, forcas, Ks, qs)
			Hs[cA] = H
			for jogador in impacto_cA:
				if type(jogador) == int:
					impactos[jogador][jogo] = [impacto_cA[jogador][0], impacto_cA[jogador][1], impacto_cA['C'], impacto_cA['tempo']]
				
			for jogador in impacto_cB:
				if type(jogador) == int:
					impactos[jogador][jogo] = [impacto_cB[jogador][0], impacto_cB[jogador][1], impacto_cB['C'], impacto_cB['tempo']]
	
	return forcas, impactos

def calcular_impacto_jogador(impactos_jogador):
	C_total_jogador = 0
	tempo_total_jogador = 0
	C_total_time = 0
	tempo_total_time = 0
	for jogo in impactos_jogador:
		C_jogador, tempo_jogador, C_time, tempo_time = impactos_jogador[jogo]
		C_total_jogador += C_jogador
		tempo_total_jogador += tempo_jogador
		C_total_time += C_time
		tempo_total_time += tempo_time
	
	return 90 * (C_total_time / tempo_total_time - (C_total_time - C_total_jogador) / (tempo_total_time - tempo_total_jogador))

def calcular_impactos(impactos):
	impactos_final = {}
	for jogador in impactos:
		impactos_final[jogador] = calcular_impacto_jogador(impactos[jogador])
	
	return impactos_final

Ks = [32 for i in range(len(jogadores))]
qs = [1 for i in range(len(jogadores))]
Hs = [20 for i in range(20)]
novas_forcas, impactos = ELO(jogos, copy(forcas), escalacoes, Ks, qs, Hs, anos)
