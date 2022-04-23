data {
  int<lower = 1> n_obs;                   // number of matches observed
  int<lower = 1> n_players;               // number of players 
  int<lower = 1> n_players_per_game;     // number of players per game
  int y[n_obs, 2];                           // data, matches results ([goals home, goals away])
  int t1[n_obs, n_players_per_game];               // time 1
  int t2[n_obs, n_players_per_game];               // time 2
  
}

parameters {
  real<lower = 0> theta1[n_players]; // model parameters {beta, gamma}
  real<lower = 0> theta2[n_players]; // model parameters {beta, gamma}
}

model {
  theta1 ~ std_normal();     // mu
  theta2 ~ std_normal();     // mu
  for (n in 1:n_obs){
    y[n, 1] ~ poisson(sum(theta1[t1[n, ]]) / sum(theta2[t2[n, ]]));
    y[n, 2] ~ poisson(sum(theta1[t2[n, ]]) / sum(theta2[t1[n, ]]));
  }
}

