library(StanHeaders)
library(ggplot2)
library(rstan)
library(parallel)
library(plotrix)

options(mc.cores = detectCores())
rstan_options(auto_write = TRUE)

# formatar os dados (talvez fazer isso em python e só carregar aqui)

# ----------------- estimação da distribuição a posteriori ------------------------#
games_data = list(n_obs = ,
                  n_players = ,
                  times = ,
                  n_players_per_game = ,
                  results = ,
                  club_1 = ,
                  club_2 = 
                  )

parameters = c('theta_1', 'theta_2')
n_chains = 8
n_warmups = 400
n_iter = 2000
n_thin = 1
model <- stan_model('bayesian_model.stan')
profic_fit = sampling(model,
          	          data = games_data,
             		  pars = parameters,
	                  chains = n_chains,
	                  warmup = n_warmups,
            	      iter = n_iter,
	                  thin = n_thin)

# salvar resultados e analisar com python
