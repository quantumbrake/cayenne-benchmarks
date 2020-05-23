#!/usr/bin/env python3

import pathlib
from subprocess import Popen, PIPE, TimeoutExpired

import click

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
    fname = f"benchmarks/{lib}-{algo}-{model}-{nrep}.json"
    benchmark_cmd = (
        f"hyperfine --runs 7 --export-json {fname} --show-output '{sim_cmd} False'"
    )
    return fname, benchmark_cmd


@click.command()
@click.option(
    "--lib",
    "-l",
    type=str,
    help="The stochastic simulation library containing the algorithm",
)
@click.option("--model", "-m", type=str, help="The DSMTS ID of the model to benchmark")
@click.option("--algo", "-a", type=str, help="The stochastic algorithm to benchmark")
@click.option(
    "--nrep",
    "-n",
    type=int,
    help="The number of repetitions in the stochastic simulation (typically ~10000)",
)
@click.option(
    "--timeout", "-t", default=10_000, type=int, help="Seconds to wait until timeout"
)
def main(lib: str, model: str, algo: str, nrep: int, timeout: int) -> None:
    """
        Benchmark a stochastic simulation for a given library (lib), model ID
        (model) and algorithm (algo).

        NOTE: You need `hyperfine` installed to run this script. It can be
        found here: https://github.com/sharkdp/hyperfine .

        Examples:

        python run_benchmarks --lib pyssa --model 00001 --algo direct --nrep 10000

        python run_benchmarks -l pyssa -m 00001 -a direct -n 10000
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
    except TimeoutExpired:
        print(f"{cmd} timeout")
        proc.kill()
        stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        print(f"{cmd} failed")


if __name__ == "__main__":
    main()
