"""
    Accuracy tests of the libraries
"""

import sys
import numpy as np

id_ = sys.argv[1]
library = sys.argv[2]
analytical_estimate = np.genfromtxt(f"data/results_{id_}.csv", skip_header=1, delimiter=",")
# analytical_estimate = analytical_estimate[:,1]
mu_analytical = analytical_estimate[:, 1]
std_analytical = analytical_estimate[:, 2]
n_rep = 10000
n_timepoints = 51
simulation_estimate = np.zeros((n_timepoints, n_rep))
for ind1 in range(1, n_rep + 1):
    temp = np.genfromtxt(f"results/{id_}/{library}/{ind1}.csv", delimiter=",")
    simulation_estimate[:, ind1 - 1] = temp[:, 1]

z_list = []
y_list = []
for ind1 in range(1, n_timepoints):
    mu_obs = np.mean(simulation_estimate[ind1, :])
    std_obs = np.std(simulation_estimate[ind1, :])
    z_list.append(
        np.sqrt(n_rep) * (mu_obs - mu_analytical[ind1]) / std_analytical[ind1]
    )
    y_list.append(np.sqrt(n_rep / 2) * ((std_obs ** 2) / (std_analytical[ind1] ** 2) - 1))

Z = np.array(z_list)
Y = np.array(y_list)

assert (-3 < Z).all()
assert (Z < 3).all()
assert (-5 < Y).all()
assert (Y < 5).all()
