#!/usr/bin/env python3

import pathlib
from subprocess import Popen, PIPE, TimeoutExpired
import sys

from run_simulations import get_cmd


def get_benchmark_cmd(lib: str, model: str, algo: str, nrep: int) -> str:
    """
        Create the benchmark command for the simulation

        Parameters
        ----------
        lib : str
            The stochastic simulation library to be used
        model : str
            The id of the model to be simulated
        algo : {direct, tau_leaping, tau_adaptive}
            The algorithm to be used for the simulations
        nrep : int
            The number of repetitions in the stochastic simulation

        Returns
        -------
        str
            The benchmark command
    """
    sim_cmd = get_cmd(lib, model, algo, nrep)
    # TODO: Add this flag to all the scripts
    fname = f"benchmarks/{lib}-{algo}-{model}-{nrep}.json"
    benchmark_cmd = (
        f"hyperfine --runs 7 --export-json {fname} --show-output '{sim_cmd} False'"
    )
    return fname, benchmark_cmd


def benchmark_simulation(
    lib: str, model: str, algo: str, nrep: int, timeout: int = 10_000
) -> None:
    """
        Benchmark the stochastic simulation

        Parameters
        ----------
        lib : str
            The stochastic simulation library to be used
        model : str
            The id of the model to be simulated
        algo : {direct, tau_leaping, tau_adaptive}
            The algorithm to be used for the simulations
        nrep : int
            The number of repetitions in the stochastic simulation
        timeout : int
            The subproces timeout value
    """
    print(
        f"Running library: {lib}, algorithm: {algo}, model: {model} with nrep = {nrep}"
    )
    fname, cmd = get_benchmark_cmd(lib, model, algo, nrep)
    fpath = pathlib.Path(fname)
    if fpath.exists() and fpath.is_file():
        print(f"Benchmarks already exist for {fpath.stem}")
        return None
    proc = Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE)
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
        # print(stdout)
        # print(stderr)
    except TimeoutExpired:
        print(f"{cmd} timeout")
        proc.kill()
        stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        print(f"{cmd} failed")


if __name__ == "__main__":
    LIB = sys.argv[1]
    MODEL = sys.argv[2]
    ALGO = sys.argv[3]
    NREP = int(sys.argv[4])
    benchmark_simulation(LIB, MODEL, ALGO, NREP)
