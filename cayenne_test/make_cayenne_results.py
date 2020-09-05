#!/usr/bin/env python3

import pathlib
import os
import sys

import numpy as np
from cayenne import Simulation

from models import get_model


def run_model(model_id, algorithm, n_rep):
    species_names, rxn_names, V_r, V_p, X0, k, max_t, max_iter, _ = get_model(model_id)
    sim = Simulation(species_names, rxn_names, V_r, V_p, X0, k)
    sim.simulate(
        algorithm=algorithm,
        max_t=max_t,
        max_iter=max_iter,
        chem_flag=False,
        n_rep=n_rep,
        debug=False,
    )
    return sim.results


def write_model(results, dir_path, n_reps):
    os.makedirs(dir_path, exist_ok=True)
    for i, (x, t, _) in enumerate(results):
        file_name = f"{dir_path}/{i + 1}.csv"
        sim = np.hstack([t.reshape(x.shape[0], 1), x])
        if x.shape[1] == 1:
            np.savetxt(file_name, sim, delimiter=",", fmt=["%.8e", "%d"])
        else:
            np.savetxt(file_name, sim, delimiter=",", fmt=["%.8e", "%d", "%d"])


if __name__ == "__main__":
    MODEL_ID = sys.argv[1]
    ALGO = sys.argv[2]
    N_REPS = int(sys.argv[3])
    WRITE_RESULTS_FLAG = sys.argv[4]
    DIR_PATH = pathlib.Path(f"./results/{MODEL_ID}/cayenne_{ALGO}/")
    results = run_model(MODEL_ID, ALGO, N_REPS)
    if WRITE_RESULTS_FLAG == "True":
        write_model(results, DIR_PATH, N_REPS)
    else:
        print("Not saving results")
