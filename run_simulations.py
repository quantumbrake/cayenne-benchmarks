#!/usr/bin/env python3

from functools import partial
import multiprocessing as mp
import pathlib
from subprocess import Popen, PIPE, TimeoutExpired
from warnings import warn

import pandas as pd

from accuracy.test_accuracy_modular import test_accuracy


def wrapper(x, func):
    return func(*x)


def get_cmd(lib, model, algo, nrep):
    if lib == "BioSimulator":
        cmd = f"julia biosimjl_test/make_biosim_results.jl {model} {algo} {nrep}"
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
        print("Results already exist")
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


def main(lib, models, algos, nrep, processes=4):
    simulation_args = []
    for model in models:
        for algo in algos:
            simulation_args.append((lib, model, algo, nrep))
    func = partial(wrapper, func=run_simulation)
    with mp.Pool(processes=processes) as pool:
        data_map = pool.map(func, simulation_args)
    cols = ["model", "lib", "algo", "nrep", "test0", "test1", "test2", "test3"]
    data_list = list(data_map)
    df = pd.DataFrame(data_list)
    print(df)
    file_name = f"{lib}_results.csv"
    df.to_csv(file_name, index=False)


if __name__ == "__main__":
    LIB = "pyssa"
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
    # ALGOS = ["tau_leaping", "tau_adaptive"]
    NREP = 10_000
    main(LIB, MODELS, ALGOS, NREP)
