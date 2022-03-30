library(StanHeaders)
library(ggplot2)
library(rstan)
library(parallel)
library(plotrix)

options(mc.cores = detectCores())
rstan_options(auto_write = TRUE)

#-----------------  geração de dados sintéticos -------------------------------------#
n_players_per_team = 22;
n_players_per_game = 11;
n_teams = 40;
n_years = 10;
n_players = n_teams * n_players_per_team;
n_obs = n_teams * (n_teams - 1) * n_years;

#---------  simula os jogos ---------------------#
# prof_players = rnorm(mean = 10, n_players); # proficiências com distribuição normal, média 10
prof_players = abs(rnorm(n_players)); # proficiências com distribuição normal, truncada no 0
t1 = matrix(nrow = n_obs, ncol = n_players_per_game);
t2 = matrix(nrow = n_obs, ncol = n_players_per_game);
teams = matrix(nrow = n_teams, ncol = n_players_per_team);

# gols de cada jogo, forma [gols mandante, gols visitante]
goals = matrix(nrow = n_obs, ncol = 2);
game = 1
for (i in 1:n_years) {
  players = sample(n_players);
  for (j in 1:n_teams) {
  	for (k in 1:n_players_per_team) {
  	  teams[j, k] = players[(j - 1) * 11 + k];
  	}
  }
  
  for (j in 1:n_teams) {
    for (k in 1:n_teams) {
      if (j != k) {
        t1[game, ] = sample(teams[j, ], n_players_per_game);
        t2[game, ] = sample(teams[k, ], n_players_per_game);
        goals[game, 1] = rpois(1, sum(prof_players[t1[game, ]]) / sum(prof_players[t2[game, ]]));
        goals[game, 2] = rpois(1, sum(prof_players[t2[game, ]]) / sum(prof_players[t1[game, ]]));
        game = game + 1
      }
    }
  }
}

#------- fim da geracao de dados sintéticos -------------------------#

# ----------------- estimação da distribuição a posteriori ------------------------#
jogos_data = list(n_obs = n_obs,
                  n_players = n_players,
                  n_players_per_game = n_players_per_game,
                  y = goals[1:n_obs, ],
                  t1 = t1,
                  t2 = t2
                  )

parameters = c("theta")
n_chains = 8
n_warmups = 400
n_iter = 2000
n_thin = 1
# set.seed(1234)

# Set initial values:
model <- stan_model('Proficiencias.stan')
profic_fit = sampling(model,
                      data = jogos_data,
                      pars = parameters,
                      chains = n_chains,
                      warmup = n_warmups,
                      iter = n_iter,
                      thin = n_thin,
                      seed = 438497)

#----------------------- analise do resultado da estimação -------------------------#
theta_medio <- summary(profic_fit)$summary[1:n_players, 'mean']; #Para coletar a mediana, pegue a coluna '50%'
theta_q25 <- summary(profic_fit)$summary[1:n_players, '25%']
theta_q75 <- summary(profic_fit)$summary[1:n_players, '75%']

asort = sort(prof_players, index.return = TRUE);

x = asort$x# - mean(asort$x)
y = theta_medio[asort$ix]# - mean(theta_medio)

plot(x = x, y = y, type = "p", col = "red", xlab = "prof reais",
     ylab = "prof estim", bg = "red", pch = 21)

lines(x=c(x[1], x[n_players]), y=c(x[1], x[n_players]), col = 'green')
#arrows(x=x, y=y, x1=x, y1=theta_q75[asort$ix]-mean(theta_medio), code=3, angle=90, col="red", lwd=1, length=0.1)
#arrows(x=x, y=y, x1=x, y1=theta_q25[asort$ix]-mean(theta_medio), code=3, angle=90, col="red", lwd=1, length=0.1)

plotCI(x = x, y = y,
	   li = theta_q25[asort$ix],# - mean(theta_medio),
	   ui = theta_q75[asort$ix],# - mean(theta_medio),
	   xlab = "prof reais", ylab = "prof estim");
	   
lines(x = c(x[1], x[n_players]), y = c(x[1], x[n_players]), col = 'green')

#plot(profic_fit, plotfun = "hist", bins = 30, pars = "theta", include = TRUE)
rho = cor.test(prof_players, theta_medio, method = 'spearman');

print('-------------------------------------------')
print(c('Numero jogadores:      ', n_players))
print(c('Numero jogadores time: ', n_players_per_team))
print(c('Número jogos         : ', n_obs))
print('-------------------------------------------')
print(c('correlacao: ', cor(prof_players, theta_medio)))
print(c('monotonicidade', rho$estimate))
#print(c('R2: ', 1 - mean((theta_medio-mean(theta_medio)-(prof_players-mean(prof_players)))^2)/(var(theta_medio)*(n_players-1)/n_players)))
print(c('R2: ', 1 - mean((theta_medio-prof_players)^2)/(var(theta_medio)*(n_players-1)/n_players)))

#lines(x=(asort$x-mean(asort$x))/sd(asort$x), y=(theta_q25[asort$ix]-mean(theta_medio))/sd(theta_medio))
#lines(x=(asort$x-mean(asort$x))/sd(asort$x), y=(theta_q75[asort$ix]-mean(theta_medio))/sd(theta_medio))
