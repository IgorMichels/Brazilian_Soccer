data {
  int<lower = 1> n_obs;
  int<lower = 1> n_players;
  int<lower = 1> times[n_obs];
  int<lower = 1> n_players_per_game;
  int results[n_obs, 2];
  int club_1[n_obs, n_players_per_game];
  int club_2[n_obs, n_players_per_game];
}

parameters {
  real<lower = 0> theta_1[n_players];
  real<lower = 0> theta_2[n_players];
}

model {
  theta_1 ~ std_normal();
  theta_2 ~ std_normal();
  for (n in 1:n_obs){
    results[n, 1] ~ poisson(sum(theta_1[club_1[n, ]]) / sum(theta_2[club_2[n, ]]) * times[n]);
    results[n, 2] ~ poisson(sum(theta_1[club_2[n, ]]) / sum(theta_2[club_1[n, ]]) * times[n]);
  }
}

