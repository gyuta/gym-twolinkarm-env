import numpy as np

def new_target():
    while True:
        x = np.random.random(2) * 2 - 1
        if np.sum(x**2) < 1:
            break
    return x