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

mu1, mu2 = 1, 2
x, y, z = 2, 1, 2
print(multivariate_normal([mu1, mu2], [[x, y], [y, z]], 10))
print(bivariate_poisson(lamb_1 = 1, lamb_2 = 1, lamb_3 = 0, size = 10))

