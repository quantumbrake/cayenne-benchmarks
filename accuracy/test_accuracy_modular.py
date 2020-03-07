import sys
from .helpers import (
    calculate_zy,
    read_results_analytical,
    read_results_simulation,
    make_plot,
)
from .helpers import (
    read_results_analytical_2sp,
    calculate_zy_2sp,
    read_results_simulation_2sp,
)
import numpy as np


def test_accuracy(id_: str, library: str, algo: str, nrep: int):
    """Test the accuracy for a given model, library, algorithm and number
    of reps.

    Parameters
    ----------
    id_
        Model id.
    library
        Name of the library.
    algo
        Name of the algorithm for that library.
    nrep
        Number of repetitions to run.

    Returns
    -------
    failed_list : List[int]
        Number of failures of each type (Z<-3, Z>3, Y<-5 and Y>5).
    """

    two_species_models = ["00030", "00031"]

    plt_name = f"plots/{library}_{algo}_{id_}_{nrep}.pdf"
    if id_ not in two_species_models:
        time_list, mu_list, std_list = read_results_analytical(id_)
        res = read_results_simulation(id_, library=library, algo=algo, n_reps=nrep)
        Z, Y, mu_obs_list, std_obs_list = calculate_zy(
            res, time_list, mu_list, std_list
        )
        make_plot(
            time_list, mu_list, std_list, mu_obs_list, std_obs_list, Z, Y, plt_name
        )
    else:
        print("Using 2 species")
        time_list, mu_list, std_list = read_results_analytical_2sp(id_)
        res = read_results_simulation_2sp(id_, library=library, algo=algo, n_reps=nrep)
        Z, Y = calculate_zy_2sp(res, time_list, mu_list, std_list)

    # TODO: Does this work for two species?
    failed_list = [None, None, None, None]
    failed_list[0] = np.sum(Z < -3)
    failed_list[1] = np.sum(Z > 3)
    failed_list[2] = np.sum(Y < -5)
    failed_list[3] = np.sum(Y > 5)

    return failed_list
