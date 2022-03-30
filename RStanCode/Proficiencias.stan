data {
  int<lower = 1> n_obs;                   // number of matches observed
  int<lower = 1> n_players;               // number of players 
  int<lower = 1> n_players_per_game;     // number of players per game
  int y[n_obs, 2];                           // data, matches results ([goals home, goals away])
  int t1[n_obs, n_players_per_game];               // time 1
  int t2[n_obs, n_players_per_game];               // time 2
  
}

parameters {
  real<lower = 0> theta[n_players]; // model parameters {beta, gamma}
}

model {
  theta ~ std_normal();     // mu
  for (n in 1:n_obs){
    y[n, 1] ~ poisson(sum(theta[t1[n, ]]) / sum(theta[t2[n, ]]));
    y[n, 2] ~ poisson(sum(theta[t2[n, ]]) / sum(theta[t1[n, ]]));
  }
}

