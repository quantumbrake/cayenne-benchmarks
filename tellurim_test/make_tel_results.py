#!/usr/bin/env python3

import sys

import numpy as np
import tellurium as te

from models import models, nreps


def te_simulation(id_="00001"):

    model = models[id_]

    te_model = te.loada(model)
    te_model.integrator = "gillespie"
    te_model.integrator.seed = 1234
    te_model.integrator.variable_step_size = False

    nrep = nreps[id_]
    points = 50

    sim_list = []
    for i in range(nrep):
        te_model.reset()
        sim = te_model.simulate(0, 50, steps=points)
        sim_list.append(sim)
        np.savetxt(f"results/{id_}/tellurium/{i + 1}.csv", np.array(sim), delimiter=",")


if __name__ == "__main__":
    MODEL_ID = sys.argv[1]
    te_simulation(MODEL_ID)
