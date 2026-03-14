import numpy as np

def intercept_resend(bit, basis):
    eve_basis = np.random.randint(0, 2)
    if eve_basis != basis:
        return np.random.randint(0, 2)
    return bit
