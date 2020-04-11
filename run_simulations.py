#!/usr/bin/env python3

from functools import partial
import multiprocessing as mp
import pathlib
from subprocess import Popen, PIPE, TimeoutExpired
import sys
from warnings import warn

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
    elif lib == "pyssa":
        cmd = f"python pyssa_test/make_pyssa_results.py {model} {algo} {nrep}"
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
        failed_list = [-1, -1, -1, -1]
    data = {
        "model": model,
        "lib": lib,
        "algo": algo,
        "nrep": nrep,
        "test0": failed_list[0],
        "test1": failed_list[1],
        "test2": failed_list[2],
        "test3": failed_list[3],
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
        else:
            raise RuntimeError("Data file contains duplicate rows")
    df.to_csv(file_name, index=False)
    return df


def main(lib, models, algos, nrep, n_procs, save_results=False):
    simulation_args = []
    for model in models:
        for algo in algos:
            simulation_args.append((lib, model, algo, nrep))
    func = partial(wrapper, func=run_simulation)
    with mp.Pool(processes=n_procs) as pool:
        data_map = pool.map(func, simulation_args)
    cols = ["model", "lib", "algo", "nrep", "test0", "test1", "test2", "test3"]
    data_list = list(data_map)
    file_name = f"results/{lib}_results.csv"
    if save_results and nrep == 10_000:
        print("Updating the results file")
        df = update_file(file_name, data_list)
    else:
        print("Not updating the results file")
    df = pd.DataFrame(data_list)
    print(df)


if __name__ == "__main__":
    N_PROCS = int(sys.argv[1])
    SAVE_RESULTS = True if sys.argv[2] == "True" else False
    LIB = "BioSimulator"
    MODELS = ["00001"]
    # MODELS = [
    #     "00001",
    #     "00003",
    #     "00004",
    #     "00005",
    #     "00011",
    #     "00020",
    #     "00021",
    #     "00022",
    #     "00023",
    #     "00030",
    #     "00031",
    #     "00037",
    #     "00038",
    #     "00039",
    # ]
    ALGOS = ["direct"]
    # ALGOS = ["direct", "tau_leaping", "tau_adaptive"]
    NREP = 10_000
    main(LIB, MODELS, ALGOS, NREP, N_PROCS, SAVE_RESULTS)
