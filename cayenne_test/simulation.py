#!/usr/bin/env python3

import sys
import time

import numpy as np
from cayenne import Simulation


def cayenne_simulation(algorithm):
    V_r = np.array([[1, 2, 0, 0], [0, 0, 1, 1], [0, 0, 0, 0]], dtype=np.int)
    V_p = np.array([[0, 0, 2, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=np.int)
    X0 = np.array([4150, 39565, 3445], dtype=np.int)
    k = np.array([1, 0.002, 0.5, 0.04])
    sim = Simulation(species_names=["A", "B", "C"], rxn_names=["1", "2", "3", "4"], V_r, V_p, X0, k)
    sim.simulate(
        algorithm=algorithm,
        max_t=10,
        max_iter=100_000_000,
        chem_flag=False,
        n_rep=200,
        n_procs=1,
        tau=0.001,
        debug=False,
    )


def plot_results(sim, algorithm):
    fig, ax = sim.plot()
    fig.savefig(f"simulation_{algorithm}.pdf")


if __name__ == "__main__":
    algorithm = sys.argv[1]
    start_time = time.time()
    sim = cayenne_simulation(algorithm)
    end_time = time.time()
    print(f"Elapsed time in seconds: {end_time - start_time}")
    # plot_results(sim, algorithm)
