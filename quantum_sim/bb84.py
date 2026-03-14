import numpy as np
from quantum_sim.attacks import intercept_resend

def simulate_bb84(n_bits=1000, eavesdrop=False, noise=0.02):
    alice_bits = np.random.randint(0, 2, n_bits)
    alice_bases = np.random.randint(0, 2, n_bits)
    bob_bases = np.random.randint(0, 2, n_bits)

    bob_results = []

    for i in range(n_bits):
        bit = alice_bits[i]

        if eavesdrop:
            bit = intercept_resend(bit, alice_bases[i])

        if np.random.rand() < noise:
            bit = 1 - bit

        if bob_bases[i] == alice_bases[i]:
            bob_results.append(bit)
        else:
            bob_results.append(np.random.randint(0, 2))

    alice_key, bob_key = [], []
    for i in range(n_bits):
        if alice_bases[i] == bob_bases[i]:
            alice_key.append(alice_bits[i])
            bob_key.append(bob_results[i])

    return np.array(alice_key), np.array(bob_key)
