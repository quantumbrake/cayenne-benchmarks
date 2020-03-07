#!/usr/bin/env python3

import pathlib
import os
import sys

import numpy as np
import tellurium as te

from models import get_model


def run_model(id_, n_reps):
    model = get_model(id_)
    te_model = te.loada(model)
    te_model.integrator = "gillespie"
    te_model.integrator.seed = 1234
    te_model.integrator.variable_step_size = True
    results = []
    for i in range(n_reps):
        te_model.reset()
        sim = te_model.simulate(0, 50)
        results.append(sim)
    return results


def write_model(results, dir_path, n_reps):
    os.makedirs(dir_path, exist_ok=True)
    for i in range(n_reps):
        sim = np.array(results[i])
        file_name = f"{dir_path}/{i + 1}.csv"
        np.savetxt(file_name, sim, delimiter=",")


if __name__ == "__main__":
    MODEL_ID = sys.argv[1]
    N_REPS = int(sys.argv[2])
    DIR_PATH = pathlib.Path(f"./results/{MODEL_ID}/Tellurium_direct/")
    results = run_model(MODEL_ID, N_REPS)
    write_model(results, DIR_PATH, N_REPS)
