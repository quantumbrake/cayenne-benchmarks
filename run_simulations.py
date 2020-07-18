#!/usr/bin/env python3

from functools import partial
import multiprocessing as mp
import pathlib
from subprocess import Popen, PIPE, TimeoutExpired
import sys

import click
import pandas as pd

from accuracy.accuracy import test_accuracy


def wrapper(x, func):
    return func(*x)


def get_cmd(lib, model, algo, nrep):
    if lib == "BioSimulator":
        cmd = f"julia biosimjl_test/make_biosim_results.jl {model} {algo} {nrep} False"
    elif lib == "BioSimulatorIntp":
        cmd = f"julia biosimjl_test/make_biosim_results.jl {model} {algo} {nrep} True"
    elif lib == "Tellurium":
        cmd = f"python tellurium_test/make_tel_results.py {model} {nrep}"
    elif lib == "GillespieSSA":
        cmd = f"Rscript GillespieSSA_test/make_gillespieSSA_results.R {model} {algo} {nrep}"
    elif lib == "cayenne":
        cmd = f"python cayenne_test/make_cayenne_results.py {model} {algo} {nrep}"
    else:
        raise ValueError(f"Unsupported library: {lib}")
    return cmd


def results_check(lib, model, algo, nrep):
    if algo:
        folder_name = f"{lib}_{algo}"
    else:
        folder_name = lib
    results_dir = pathlib.Path(f"results/{model}/{folder_name}")
    if results_dir.is_dir():
        files = list(results_dir.iterdir())
    else:
        files = []
    if len(files) >= nrep:
        check = True
    else:
        check = False
    return check


def run_simulation(lib, model, algo, nrep, timeout=10_000):
    print(
        f"Running library: {lib}, algorithm: {algo}, model: {model} with nrep = {nrep}"
    )
    if not results_check(lib, model, algo, nrep):
        cmd = get_cmd(lib, model, algo, nrep)
        proc = Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE)
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
        except TimeoutExpired:
            print(f"{cmd} timeout")
            proc.kill()
            stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            print(f"{cmd} failed")
    else:
        print(f"Results already exist for {lib}, {algo}, {model}")
    try:
        failed_list = test_accuracy(model, lib, algo, nrep)
    except OSError:
        failed_list = [-1, -1, -1, -1, -1, -1, -1, -1]
    data = {
        "model": model,
        "lib": lib,
        "algo": algo,
        "nrep": nrep,
        "test0": failed_list[0],
        "test1": failed_list[1],
        "test2": failed_list[2],
        "test3": failed_list[3],
        "rtest0": failed_list[4],
        "rtest1": failed_list[5],
        "rtest2": failed_list[6],
        "rtest3": failed_list[7],
    }
    return data


def update_file(file_name, data_list):
    df = pd.read_csv(file_name, dtype={"model": str})
    condn = lambda x, y, z: (df["model"] == x) & (df["lib"] == y) & (df["algo"] == z)
    for data_item in data_list:
        model = data_item["model"]
        lib = data_item["lib"]
        algo = data_item["algo"]
        row = df.loc[condn(model, lib, algo)]
        if row.shape[0] == 0:
            df = df.append(data_item, ignore_index=True)
        elif row.shape[0] == 1:
            df.loc[row.index, "test0"] = data_item["test0"]
            df.loc[row.index, "test1"] = data_item["test1"]
            df.loc[row.index, "test2"] = data_item["test2"]
            df.loc[row.index, "test3"] = data_item["test3"]
            df.loc[row.index, "rtest0"] = data_item["rtest0"]
            df.loc[row.index, "rtest1"] = data_item["rtest1"]
            df.loc[row.index, "rtest2"] = data_item["rtest2"]
            df.loc[row.index, "rtest3"] = data_item["rtest3"]
        else:
            raise RuntimeError("Data file contains duplicate rows")
    df.to_csv(file_name, index=False)
    return df


@click.command()
@click.option(
    "--lib",
    "-l",
    type=str,
    help="The stochastic simulation library. Supported libraries: cayenne, BioSimulator, BioSimulatorIntp, GillespieSSA, Tellurium.",
)
@click.option(
    "--models",
    "-m",
    multiple=True,
    help="The DSMTS ID of the model to simulate. Specify multiple with additional -m tags (see example above).",
)
@click.option(
    "--algos",
    "-a",
    multiple=True,
    help="The stochastic algorithms to be used. Specify multiple with additional -a tags (see example above). Supported algorithms: direct, tau_leaping, tau_adaptive.",
)
@click.option(
    "--nrep", "-n", type=int, help="The number of repetitions in the simulation"
)
@click.option(
    "--nprocs",
    "-p",
    type=int,
    help="The number of CPU processes to use for accuracy test.",
)
@click.option("--save/--no-save", default=False, help="Save results of the simulation")
def main(lib: str, models: list, algos: list, nrep: int, nprocs: int, save: bool):
    """
        Run stochastic simulations for the library (lib), model IDs (models) and algorithms (algos).

        Examples:

        python run_simulations.py --lib cayenne --models 00001 --models 00003 --algos direct --algos tau_leaping --nrep 10000 --nprocs 4 --save

        python run_simulations.py -l cayenne -m 00001 -m 00003 -a direct -a tau_leaping -n 10000 -p 4 --save
    """
    simulation_args = []
    for model in models:
        for algo in algos:
            simulation_args.append((lib, model, algo, nrep))
    func = partial(wrapper, func=run_simulation)
    with mp.Pool(processes=nprocs) as pool:
        data_map = pool.map(func, simulation_args)
    data_list = list(data_map)
    file_name = f"results/{lib}_results.csv"
    if save and nrep == 10_000:
        print("Updating the results file")
        df = update_file(file_name, data_list)
    else:
        print("Not updating the results file")
    df = pd.DataFrame(data_list)
    print(df)


if __name__ == "__main__":
    main()
