from numpy.random import poisson, multivariate_normal
from glob import glob

import os
import json
import numpy as np
import matplotlib.pyplot as plt

def bivariate_poisson(lamb_1 = 1, lamb_2 = 1, lamb_3 = 0, size = 1):
    X_1 = poisson(lamb_1, size)
    X_2 = poisson(lamb_2, size)
    X_3 = poisson(lamb_3, size)
    Y_1 = X_1 + X_3
    Y_2 = X_2 + X_3
    
    return np.vstack([Y_1, Y_2]).T

def is_positive_semidefinite(x, y, z):
    t1 = x + z - (x**2 - 2 * x * z + 4 * y**2 + z**2)**(1/2) >= 0
    t2 = x + z + (x**2 - 2 * x * z + 4 * y**2 + z**2)**(1/2) >= 0
    
    return t1 * t2

def games_probs(lamb_1 = 1, lamb_2 = 1, lamb_3 = 0, size = 100000):
    sims = bivariate_poisson(lamb_1, lamb_2, lamb_3, size)
    w = round(sum(np.greater(sims[:, 0], sims[:, 1])) / size, 4)
    l = round(sum(np.less(sims[:, 0], sims[:, 1])) / size, 4)
    d = round(1 - w - l, 4)

    return w, d, l
    
def games_results(lamb_1 = 1, lamb_2 = 1, lamb_3 = 0, size = 100000):
    sims = bivariate_poisson(lamb_1, lamb_2, lamb_3, size)
    R = np.zeros(np.max(sims, 0) + 1)
    for sim in sims:
        R[sim[0], sim[1]] += 1
    
    R = R / size
    w = round(np.sum(np.tril(R, -1)), 6)
    d = round(np.sum(np.diag(R)), 6)
    l = round(np.sum(np.triu(R, 1)), 6)
    
    return R, (w, d, l)

# mu1, mu2 = 1, 2
# x, y, z = 2, 1, 2
# print(multivariate_normal([mu1, mu2], [[x, y], [y, z]], 100000))

n = 1000000
# probs = games_probs(lamb_1 = 2, lamb_2 = 1, lamb_3 = 0, size = n)
results, probs = games_results(lamb_1 = 2, lamb_2 = 1, lamb_3 = 0, size = n)

print(probs)

