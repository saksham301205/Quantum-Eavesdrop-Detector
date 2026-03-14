import numpy as np
from scipy.stats import entropy

def extract_features(alice_key, bob_key):
    qber = np.mean(alice_key != bob_key)
    counts = np.bincount(bob_key, minlength=2)
    probs = counts / np.sum(counts)
    ent = entropy(probs)
    return [qber, ent, len(alice_key)]
