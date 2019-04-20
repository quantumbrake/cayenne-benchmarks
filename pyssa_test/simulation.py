import sys

import numpy as np
import matplotlib.pyplot as plt
from pyssa import Simulation

algorithm = sys.argv[1]

V_r = np.array([[1, 2, 0, 0], [0, 0, 1, 1], [0, 0, 0, 0]])
V_p = np.array([[0, 0, 2, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
X0 = np.array([4150, 39565, 3445])
k = np.array([1, 0.002, 0.5, 0.04])

sim = Simulation(V_r, V_p, X0, k)
sim.simulate(
    algorithm=algorithm,
    max_t=10,
    max_iter=100_000_000,
    chem_flag=False,
    n_rep=10,
    n_procs=4,
    tau=0.001,
)

fig, ax = sim.plot()
fig.savefig(f"simulation_{algorithm}.pdf")
