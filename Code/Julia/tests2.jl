using Plots;
using Optim;
using Random;
using StatsBase;
using Statistics;
using Distributions;
using LinearAlgebra;

function creat_players(clubs, players_per_club, mean = 0, var = 1, lb = 0, ub = 100)
    all_players = rand(Truncated(Normal(mean, var), lb, ub), (2 * clubs * players_per_club, 2));
    all_players[:, 1] = all_players[:, 1] / (sum(all_players[:, 1]) / clubs);
    all_players[:, 2] = all_players[:, 2] / (sum(all_players[:, 2]) / clubs);
    players = Dict{Int64, Vector{Float64}}();
    for i in 1:(clubs * players_per_club)
        players[i] = all_players[i, :];
    end
    return players
end;

function simulating_game(λatk₁, λatk₂, λdef₁, λdef₂, sims = 1000000)
    X₁ = Poisson(λatk₁ / λdef₂);
    X₂ = Poisson(λatk₂ / λdef₁);
    Y₁ = rand(X₁, sims);
    Y₂ = rand(X₂, sims);
    wins₁ = sum(Y₁ .> Y₂);
    draws = sum(Y₁ .== Y₂);
    wins₂ = sum(Y₁ .< Y₂);
    return wins₁, draws, wins₂
end;

function create_games(seasons, clubs, ppc)
    results = [[[0 for i in 1:4] for j in 1:clubs * (clubs - 1)] for s in 1:seasons];
    players = creat_players(clubs, ppc);
    squads = [];
    for s in 1:seasons
        line = 1;
        append!(squads, [reshape(shuffle(collect(1:length(players))), (clubs, ppc))]);
        clubs_atks = convert(Matrix{Float64}, (deepcopy(last(squads))));
        clubs_defs = convert(Matrix{Float64}, (deepcopy(last(squads))));
        for i in 1:clubs
            for j in 1:ppc
                clubs_atks[i, j] = players[clubs_atks[i, j]][1];
                clubs_defs[i, j] = players[clubs_defs[i, j]][2];
            end
        end

        for j in 1:clubs
            for k in 1:clubs
                if j != k
                    Xⱼ = Poisson(sum(clubs_atks[j, :]) / sum(clubs_defs[k, :]));
                    Xₖ = Poisson(sum(clubs_atks[k, :]) / sum(clubs_defs[j, :]));
                    results[s][line][1] = j;
                    results[s][line][2] = rand(Xⱼ);
                    results[s][line][3] = rand(Xₖ);
                    results[s][line][4] = k;
                    line += 1;
                end
            end
        end
    end
    return results, squads, players;
end;

function likelihood(players, results, squads)
    if typeof(players) != Dict{Int64, Vector{Float64}}
        all_players = Dict{Int64, Vector{Float64}}();
        if size(players, 2) != 2
            players = reshape(players, (Int(length(players) // 2), 2));
        end
        
        for i in 1:size(players, 1)
            all_players[i] = players[i, :];
        end
    else
        all_players = players;
    end
    loglikelihood = 0
    for i in 1:length(squads)
        clubs, ppc = size(squads[i]);
        clubs_atks = convert(Matrix{Float64}, (deepcopy(squads[i])));
        clubs_defs = convert(Matrix{Float64}, (deepcopy(squads[i])));
        for j in 1:size(squads[i], 1)
            for k in 1:size(squads[i], 2)
                clubs_atks[j, k] = all_players[squads[i][j, k]][1];
                clubs_defs[j, k] = all_players[squads[i][j, k]][2];
            end
        end
        for j in 1:length(results[i])
            clubₕ, kₕ, kₐ, clubₐ = results[i][j]
            loglikelihood -= logpdf(Poisson(sum(clubs_atks[clubₕ, :]) / sum(clubs_defs[clubₐ, :])), kₕ);
            loglikelihood -= logpdf(Poisson(sum(clubs_atks[clubₐ, :]) / sum(clubs_defs[clubₕ, :])), kₐ);
        end
    end
    
    return loglikelihood;
end

function gradient(players, results, squads)
    if typeof(players) != Dict{Int64, Vector{Float64}}
        all_players = Dict{Int64, Vector{Float64}}();
        if size(players, 2) != 2
            players = reshape(players, (Int(length(players) // 2), 2));
        end
        
        for i in 1:size(players, 1)
            all_players[i] = players[i, :];
        end
    else
        all_players = players;
    end
    p = length(all_players);
	∇likelihood = zeros(2 * length(all_players));
    for season in 1:length(results)
        for game in 1:length(results[season])
            clubₕ, kₕ, kₐ, clubₐ = results[season][game];
            λ₁ₕ, λ₁ₐ, λ₂ₕ, λ₂ₐ = 0, 0, 0, 0;
            Cₕ, Cₐ = squads[season][clubₕ, :], squads[season][clubₐ, :];
            for k in 1:size(squads[season], 2)
                λ₁ₕ += all_players[Cₕ[k]][1];
                λ₁ₐ += all_players[Cₐ[k]][1];
                λ₂ₕ += all_players[Cₕ[k]][2];
                λ₂ₐ += all_players[Cₐ[k]][2];
            end
            
            for i in 1:p
                j = i + p
                		∇likelihood[i] -= (kₕ/λ₁ₕ - 1 / λ₂ₐ) * (i in Cₕ);
                		∇likelihood[i] -= (kₐ/λ₁ₐ - 1 / λ₂ₕ) * (i in Cₐ);
                		∇likelihood[j] -= (- kₕ/λ₂ₐ + λ₁ₕ / (λ₂ₐ^2)) * (i in Cₐ);
                		∇likelihood[j] -= (- kₐ/λ₂ₕ + λ₁ₐ / (λ₂ₕ^2)) * (i in Cₕ);
            end
        end
    end
    
    return ∇likelihood;
end;

results, squads, players = create_games(10, 20, 11);
l_o = likelihood(players, results, squads);
g_o = gradient(players, results, squads);

f(x) = likelihood(x, results, squads)
g(lik, x) = gradient(x, results, squads)
lower = zeros(2 * 220)
upper = 20 * ones(2 * 220)
x_inicial = rand(2 * 220)
od = OnceDifferentiable(f, g, x_inicial)
@time res1  = optimize(od,
                       lower,
                       upper,
                       x_inicial,
                       Fminbox(GradientDescent()),
                       Optim.Options(iterations = 1000))
@time res2  = optimize(od,
                       lower,
                       upper,
                       x_inicial,
                       Fminbox(NelderMead()),
                       Optim.Options(iterations = 1000))
@time res3 = optimize(x -> likelihood(x, results, squads),
                      lower,
                      upper,
                      x_inicial,
                      Fminbox(NelderMead()),
                      Optim.Options(iterations = 1000))

println("finalizou!")
println(Optim.converged(res1), " ", Optim.minimum(res1), " ", l_o)
println(Optim.converged(res2), " ", Optim.minimum(res2), " ", l_o)
println(Optim.converged(res3), " ", Optim.minimum(res3), " ", l_o)
