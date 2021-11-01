import numpy as np

def new_target():
    while True:
        x = np.random.random(2) * 4 - 2
        if np.sum(x**2) < 8:
            break
    return x