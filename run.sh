#!/usr/bin/env bash

set -e

echo "pyssa direct"
python pyssa_test/simulation.py "direct"
echo "pyssa tau_leaping"
python pyssa_test/simulation.py "tau_leaping"
echo "pyssa tau_adaptive"
python pyssa_test/simulation.py "tau_adaptive"
echo "tellurium"
python -W ignore tellurim_test/simulation.py
echo "biomsim.jl"
julia --procs=1 biosimjl_test/model1.jl
echo "GillespieSSA.R"
# Rscript GillespieSSA_test/simulation.R
