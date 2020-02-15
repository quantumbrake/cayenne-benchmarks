#!/usr/bin/env python3

import pathlib
import os
import sys

import numpy as np
import tellurium as te

from models import get_model

N_REPS = 10_000


def run_model(id_):
    model = get_model(id_)
    te_model = te.loada(model)
    te_model.integrator = "gillespie"
    te_model.integrator.seed = 1234
    te_model.integrator.variable_step_size = True
    results = []
    for i in range(N_REPS):
        te_model.reset()
        sim = te_model.simulate(0, 50)
        results.append(sim)
    return results

def write_model(results, dir_path):
    os.makedirs(dir_path, exist_ok=True)
    for i in range(N_REPS):
        sim = np.array(results[i])
        file_name = f"{dir_path}/{i + 1}.csv"
        np.savetxt(file_name, sim, delimiter=",")


if __name__ == "__main__":
    MODEL_ID = sys.argv[1]
    DIR_PATH = pathlib.Path(f"./results/{MODEL_ID}/tellurim/")
    results = run_model(MODEL_ID)
    write_model(results, DIR_PATH)
