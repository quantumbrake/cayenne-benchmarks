import pathlib
from typing import Tuple

import numpy as np
import pandas as pd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerPatch
from matplotlib.lines import Line2D

from cayenne.results import Results


def read_results_analytical(test_id: str):
    """
        Read the simulation results used for accuracy tests.

        Parameters
        ----------
        test_id: str
            The index of the test number to return the results of.

        Returns
        -------
        time_list: List[float]
            Time points at which species amounts are analytically predicted.
        mu_list: List[float]
            Time course of the analytically predicted species amount means.
        std_list: List[float]
            Time course of the analytically predicted species amount standard
            deviations.

        See Also
        --------
        read_results_analytical_2sp: Read results for 2 species.

        Notes
        -----
        The accuracy tests are taken from the SBML Test Suite [1]_ .

        References
        ----------
        .. [1] https://github.com/sbmlteam/sbml-test-suite/tree/master/cases/stochastic
    """
    filename = f"data/results_{test_id}.csv"
    # time,X-mean,X-sd
    data = pd.read_csv(filename)
    time = data["time"].values
    mu = data["X-mean"].values
    std = data["X-sd"].values
    return time, mu, std


def read_results_analytical_2sp(test_id: str):
    """
        Read the simulation results used for accuracy tests when 2 species
        are tracked.

        Parameters
        ----------
        test_id: str
            The index of the test number to return the results of.

        Returns
        -------
        time_list: List[float]
            Time points at which species amounts are analytically predicted.
        mu_list: List[float]
            Time course of the analytically predicted species amount means.
        std_list: List[float]
            Time course of the analytically predicted species amount standard
            deviations.

        See Also
        --------
        read_results_analytical: Read results for one species.

        Notes
        -----
        The accuracy tests are taken from the SBML Test Suite [1]_ .

        References
        ----------
        .. [1] https://github.com/sbmlteam/sbml-test-suite/tree/master/cases/stochastic
    """
    filename = f"data/results_{test_id}.csv"
    # time, X-mean, X-sd
    data = pd.read_csv(filename)
    time = data["time"].values
    p_mean = data["P-mean"].values.reshape(-1, 1)
    p2_mean = data["P2-mean"].values.reshape(-1, 1)
    mu = np.hstack([p_mean, p2_mean])
    p_sd = data["P-sd"].values.reshape(-1, 1)
    p2_sd = data["P2-sd"].values.reshape(-1, 1)
    std = np.hstack([p_sd, p2_sd])
    return time, mu, std


def get_results_from_index(res: Results, ind: int):
    """Get simulation states at given index.

    Parameters
    ----------
    res
        A cayenne.Results object.
    ind
        The index to return simulation states at. 0 will return the first
        time point.
    """
    states = []
    for i in range(len(res)):
        # for each repetition
        x_rep, _, _ = res[i]
        if ind >= x_rep.shape[0]:
            state = x_rep[-1]
        else:
            state = x_rep[ind]
        states.append(state)
    return states


def calculate_zy(
    res: Results,
    time_arr: np.array,
    mu_analytical: np.array,
    std_analytical: np.array,
    saved_results_interpolated: bool,
):
    """Calculate Z and Y.

    For a given simulation result and the analytical mean and standard
    deviations, compute the Z and Y statistics for each time point.

    Parameters
    ----------
    res
        A cayenne.Results object.
    time_arr
        List of time points at which analytical solutions are available.
    mu_analytical
        List of analytical means at the time points in ``time_arr``.
    std_analytical
        List of analytical standard deviations at the time points in
        ``time_arr``.
    saved_results_interpolated
        Flag denoting whether saved simulation results are interpolated or not.
        ``True`` if interpolated.

    Returns
    -------
    z_arr
        Numpy array of calculated Z values.
    y_arr
        Numpy array of calculated Y values.
    mu_obs_arr
        Numpy array of observed mean values.
    std_obs_arr
        Numpy array of observed standard deviation values.
    """
    z_list = []
    y_list = []
    n_rep = len(res.t_list)
    mu_obs_arr = np.zeros(len(time_arr))
    std_obs_arr = np.zeros(len(time_arr))
    mu_obs_arr[0] = mu_analytical[0]
    for ind1, t in enumerate(time_arr[1:]):
        if saved_results_interpolated == False:
            results = res.get_state(t)
        else:
            results = get_results_from_index(res, ind1 + 1)
        mu_obs = np.mean(results)
        std_obs = np.std(results)
        z_list.append(
            np.sqrt(n_rep)
            * (mu_obs - mu_analytical[ind1 + 1])
            / std_analytical[ind1 + 1]
        )
        y_list.append(
            np.sqrt(n_rep / 2) * ((std_obs ** 2) / (std_analytical[ind1 + 1] ** 2) - 1)
        )
        mu_obs_arr[ind1 + 1] = mu_obs
        std_obs_arr[ind1 + 1] = std_obs
    z_arr = np.array(z_list)
    y_arr = np.array(y_list)
    return z_arr, y_arr, mu_obs_arr, std_obs_arr


def calculate_ms_ratios(
    mu_obs: np.array,
    mu_analytical: np.array,
    std_obs: np.array,
    std_analytical: np.array,
) -> Tuple[np.array, np.array]:
    """
        Calculate mu and sigma ratios

        Parameters
        ----------
        mu_obs : np.array
        mu_analytical : np.array
        std_obs : np.array
        std_analytical : np.array

        Returns
        -------
        Tuple[np.array, np.array]
    """
    mu_ratio = mu_obs / mu_analytical
    mu_ratio[np.where(mu_ratio == np.inf)] = 1.0
    std_ratio = std_obs / std_analytical
    std_ratio[np.where(std_ratio == np.inf)] = 1.0
    return mu_ratio, std_ratio


def calculate_zy_2sp(
    res: Results,
    time_arr: np.array,
    mu_analytical: np.array,
    std_analytical: np.array,
    saved_results_interpolated: bool,
):
    """Calculate Z and Y for simulations with 2 species.

    For a given simulation result and the analytical mean and standard
    deviations, compute the Z and Y statistics for each time point.

    Parameters
    ----------
    res
        A cayenne.Results object.
    time_arr
        List of time points at which analytical solutions are available.
    mu_analytical
        List of analytical means at the time points in ``time_arr``.
    std_analytical
        List of analytical standard deviations at the time points in
        ``time_arr``.
    saved_results_interpolated
        Flag denoting whether saved simulation results are interpolated or not.
        ``True`` if interpolated.

    Returns
    -------
    z_arr
        Numpy array of calculated Z values.
    y_arr
        Numpy array of calculated Y values.
    mu_obs_arr
        Numpy array of observed mean values.
    std_obs_arr
        Numpy array of observed standard deviation values.
    """
    z_list = []
    y_list = []
    n_rep = len(res.t_list)
    mu_obs_list = [mu_analytical[0, :]]
    std_obs_list = [[0.0, 0.0]]
    for ind1, t in enumerate(time_arr[1:]):
        if not saved_results_interpolated:
            results = res.get_state(t)
        else:
            results = get_results_from_index(res, ind1 + 1)
        mu_obs = np.mean(results, axis=0)
        std_obs = np.std(results, axis=0)
        z_list.append(
            np.sqrt(n_rep)
            * (mu_obs - mu_analytical[ind1 + 1, :])
            / std_analytical[ind1 + 1, :]
        )
        y_list.append(
            np.sqrt(n_rep / 2)
            * ((std_obs ** 2) / (std_analytical[ind1 + 1, :] ** 2) - 1)
        )
        mu_obs_list.append(mu_obs)
        std_obs_list.append(std_obs)
    z_arr = np.array(z_list)
    y_arr = np.array(y_list)
    mu_obs_arr = np.array(mu_obs_list)
    std_obs_arr = np.array(std_obs_list)
    return z_arr, y_arr, mu_obs_arr, std_obs_arr


def get_highest_rep_in_path(this_path: str):
    p = pathlib.Path(this_path)
    file_list = list(p.iterdir())
    highest_rep = len(file_list)
    print(f"{highest_rep} reps detected, returning results from all.")
    return highest_rep


def read_results_simulation(
    model: str = "00001",
    library: str = "GillespieSSA",
    algo: str = "direct",
    n_reps: str = None,
    res_folder: str = None,
):
    """Read simulation results.

    Given a model, library and algorithm, read the results. If `n_reps` is also
    provided, read only the first `n_rep` results. If not, read as many as
    there are in the folder for that model/library/algorithm combination.

    Parameters
    ----------
    model
        Model id.
    library
        Name of the library.
    algo
        Name of the algorithm.
    n_reps
        Number of reps to read the simulation results for. Default is `None`
        and all results are read.
    res_folder
        If None, read from the results folder. Else read from the specified
        folder. This is used in tests.

    Returns
    -------
    res: Results
        A `cayenne.Results` object containing the results.
    """
    x_list = []
    t_list = []
    status_list = []
    sim_seeds = []
    if res_folder is None:
        res_folder = f"results/{model}/{library}_{algo}/"
    if n_reps is None:
        n_reps = get_highest_rep_in_path(res_folder)

    for rep_no in range(1, n_reps + 1):
        contents = pd.read_csv(res_folder + f"{rep_no}.csv", names=["time", "S1"])
        t_list.append(contents["time"].values)
        x_list.append(contents["S1"].values.reshape(contents.shape[0], 1))
        status_list.append(0)
        sim_seeds.append(0)
    species_names = [f"species_{i}" for i in range(x_list[0].shape[1])]
    rxn_names = ["X"]
    res = Results(
        species_names, rxn_names, t_list, x_list, status_list, algo, sim_seeds
    )
    return res


def read_results_simulation_2sp(
    model="00030",
    library="GillespieSSA",
    algo="direct",
    n_reps=None,
    res_folder: str = None,
):
    """Read simulation results for 2sp.

    Given a model, library and algorithm, read the results. If `n_reps` is also
    provided, read only the first `n_rep` results. If not, read as many as
    there are in the folder for that model/library/algorithm combination.

    Parameters
    ----------
    model
        Model id.
    library
        Name of the library.
    algo
        Name of the algorithm.
    n_reps
        Number of reps to read the simulation results for. Default is `None`
        and all results are read.
    res_folder
        If None, read from the results folder. Else read from the specified
        folder. This is used in tests.

    Returns
    -------
    res: Results
        A `cayenne.Results` object containing the results.
    """
    x_list = []
    t_list = []
    status_list = []
    sim_seeds = []
    if res_folder is None:
        res_folder = f"results/{model}/{library}_{algo}/"
    if n_reps is None:
        n_reps = get_highest_rep_in_path(res_folder)

    for rep_no in range(1, n_reps + 1):
        contents = pd.read_csv(res_folder + f"{rep_no}.csv", names=["time", "S1", "S2"])
        t_list.append(contents["time"].values)
        x_list.append(contents[["S1", "S2"]].values)
        status_list.append(0)
        sim_seeds.append(0)
    res = Results(t_list, x_list, status_list, algo, sim_seeds)
    return res


def make_zy_plot(
    time_pts: np.array,
    value_obs: np.array,
    value_analytical: np.array,
    stat: np.array,
    stat_thresh: float,
    ax,
):
    """Make an overlay plot.

    Overlay the analytical and observed values across time. Color the
    points which violate statistical thresholds differently.

    Parameters
    ----------
    time_pts
        Numpy array of time points.
    value_obs
        Observed values at each time point.
    value_analytical
        Analytical values at each time point.
    stat
        Statistic at each time point.
    stat_thresh
        Statistic threshold to color by, same for all time points.
    ax
        Axis object to plot on.
    """
    ax.plot(time_pts, value_analytical)
    for i in range(len(stat)):
        if -stat_thresh <= stat[i] <= stat_thresh:
            marker = "green"
        else:
            marker = "red"
        ax.plot(time_pts[i + 1], value_obs[i + 1], ".", color=marker)


# NOTE: Use calculate_ms_ratios function instead
def make_ratio_plot(
    time_pts: np.array,
    value_obs: np.array,
    value_analytical: np.array,
    stat_thresh: list,
    ax,
):
    """Make a plot of ratios of observed means to analytical means

    """
    stat_lb, stat_ub = stat_thresh[0], stat_thresh[1]
    ax.axhline(y=1.0, alpha=0.8, color="black")
    ax.axhline(y=stat_lb, linestyle="--", color="black")
    ax.axhline(y=stat_ub, linestyle="--", color="black")
    for i in range(time_pts.shape[0]):
        obs, analytical = value_obs[i], value_analytical[i]
        try:
            ratio = obs / analytical
        except ZeroDivisionError:
            continue
        if stat_lb <= ratio <= stat_ub:
            marker = "green"
        else:
            marker = "red"
        ax.plot(time_pts[i], ratio, ".", color=marker)


def make_plot(
    time_arr: np.array,
    mu_analytical: np.array,
    std_analytical: np.array,
    mu_obs: np.array,
    std_obs: np.array,
    Z: np.array,
    Y: np.array,
    plt_name: str,
):
    """Plot simulations vs original values.

    Make a plot to compare simulations vs original values.

    Parameters
    ----------
    time_arr
        List of time points at which analytical solutions are available.
    mu_analytical
        List of analytical means at the time points in ``time_arr``.
    std_analytical
        List of analytical standard deviations at the time points in
        ``time_arr``.
    mu_obs
        Numpy array of observed mean values.
    std_obs
        Numpy array of observed standard deviation values.
    Z
        Numpy array of calculated Z values.
    Y
        Numpy array of calculated Y values.
    """
    fig, ax = plt.subplots(2, 2, sharex="col", constrained_layout=True)
    name = plt_name.split("/")[1].split(".")[0]
    fig.suptitle(name)
    make_zy_plot(time_arr, mu_obs, mu_analytical, Z, 3, ax[0, 0])
    ax[0, 0].set_ylabel(r"$\mu$")
    make_zy_plot(time_arr, std_obs, std_analytical, Y, 5, ax[0, 1])
    ax[0, 1].set_ylabel(r"$\sigma$")
    make_ratio_plot(time_arr, mu_obs, mu_analytical, [0.98, 1.02], ax[1, 0])
    ax[1, 0].set_ylabel(r"$\mu$ ratio")
    ax[1, 0].set_xlabel("time")
    make_ratio_plot(time_arr, std_obs, std_analytical, [0.98, 1.02], ax[1, 1])
    ax[1, 1].set_ylabel(r"$\sigma$ ratio")
    ax[1, 1].set_xlabel("time")
    green_patch = Line2D(
        [0], [0], marker=".", color="w", markerfacecolor="green", markersize=15
    )
    red_patch = Line2D(
        [0], [0], marker=".", color="w", markerfacecolor="red", markersize=15
    )
    analytical_patch = Line2D([0], [0])
    ratio_patch = Line2D([0], [0], color="black")
    ratioborder_patch = Line2D([0], [0], linestyle="--", color="black")
    text_labels = [
        "Accurate (Simulation)",
        "Inaccurate (Simulation)",
        "Analytical solution",
        "Ratio (expected)",
        "Ratio (threshold)",
    ]
    lgd = fig.legend(
        [green_patch, red_patch, analytical_patch, ratio_patch, ratioborder_patch],
        text_labels,
        loc="upper left",
        bbox_to_anchor=(1.02, 0.9),
        fontsize="small",
    )
    fig.savefig(plt_name, bbox_extra_artists=(lgd,), bbox_inches="tight")


def make_plot_2sp(
    time_arr: np.array,
    mu_analytical: np.array,
    std_analytical: np.array,
    mu_obs: np.array,
    std_obs: np.array,
    Z: np.array,
    Y: np.array,
    plt_name: str,
):
    """Plot simulations vs original values.

    Make a plot to compare simulations vs original values.

    Parameters
    ----------
    time_arr
        List of time points at which analytical solutions are available.
    mu_analytical
        List of analytical means at the time points in ``time_arr``.
    std_analytical
        List of analytical standard deviations at the time points in
        ``time_arr``.
    mu_obs
        Numpy array of observed mean values.
    std_obs
        Numpy array of observed standard deviation values.
    Z
        Numpy array of calculated Z values.
    Y
        Numpy array of calculated Y values.
    """
    fig, ax = plt.subplots(4, 2, sharex="col", figsize=(8, 16), constrained_layout=True)
    name = plt_name.split("/")[1].split(".")[0]
    fig.suptitle(name)
    make_zy_plot(time_arr, mu_obs[:, 0], mu_analytical[:, 0], Z[:, 0], 3, ax[0, 0])
    ax[0, 0].set_ylabel("Observed mean - S1")
    make_zy_plot(time_arr, std_obs[:, 0], std_analytical[:, 0], Y[:, 0], 5, ax[0, 1])
    ax[0, 1].set_ylabel("Observed sd - S1")
    make_ratio_plot(time_arr, mu_obs[:, 0], mu_analytical[:, 0], [0.98, 1.02], ax[1, 0])
    ax[1, 0].set_ylabel(r"$\mu$ ratio - S1")
    make_ratio_plot(
        time_arr, std_obs[:, 0], std_analytical[:, 0], [0.98, 1.02], ax[1, 1]
    )
    ax[1, 1].set_ylabel(r"$\sigma$ ratio - S1")
    make_zy_plot(time_arr, mu_obs[:, 1], mu_analytical[:, 1], Z[:, 1], 3, ax[2, 0])
    ax[2, 0].set_ylabel("Observed mean - S2")
    make_zy_plot(time_arr, std_obs[:, 1], std_analytical[:, 1], Y[:, 1], 5, ax[2, 1])
    ax[2, 1].set_ylabel("Observed sd - S2")
    make_ratio_plot(time_arr, mu_obs[:, 1], mu_analytical[:, 1], [0.98, 1.02], ax[3, 0])
    ax[3, 0].set_ylabel(r"$\mu$ ratio - S2")
    ax[3, 0].set_xlabel("time")
    make_ratio_plot(
        time_arr, std_obs[:, 1], std_analytical[:, 1], [0.98, 1.02], ax[3, 1]
    )
    ax[3, 1].set_ylabel(r"$\sigma$ ratio - S2")
    ax[3, 1].set_xlabel("time")
    fig.savefig(plt_name)
