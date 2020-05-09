# Goal

The goal of this repository is to compare the different softwares used for stochastic / Gillespie type simulations (see below) on two fronts

- Accuracy of simulation
- Speed of simulation

## Background
Stochastic simulations (see [Wikipedia](https://en.wikipedia.org/wiki/Gillespie_algorithm)) are used to model biological processes or chemical reactions when the corresponding differential equations cannot be applied. This may be the case when the number of species being modeled is very small (such as 10s of molecules/biological species), and the randomness becomes important. A simple example is a starting with a small number of bacteria (say 5) in a dish. They may either all die out, or they may start dividing and growing rapidly. The outcome itself is random, and you would use a Gillespie simulator to model such a process.


## Libraries compared

We compare the 4 libraries across Python, R and Julia. These are listed below along with the algorithms in each library.

Library | Language | Algorithm name in library | Algorithm name in our comparison | Standard name of algorithm
---| --- | --- | --- | ----
pyssa | Python | `direct` | `direct` | Gillespie's Direct method ([Gillespie1973][direct])
| | | `tau_leaping` | `tau_leaping` | Standard tau leaping ([Gillespie2001][tau_leaping] also see [Wikipedia][tau_leaping_wiki])
| | | `tau_adaptive` | `tau_adaptive` | Tau leaping with efficient step size selection ([Cao. et al. 2006][tau_adaptive])
Tellurium | Python | `gillespie` | `direct` | Unknown (see [here](https://tellurium.readthedocs.io/en/latest/_notebooks/core/tellurium_stochastic.html?highlight=gillespie#stochastic-simulation)), likely similar to Gillespie's Direct Method
GillespieSSA | R | `ssa.d` | `direct` | Gillespie's Direct method ([Gillespie1973][direct])
| | | `ssa.etl` | `tau_leaping` |  Standard tau leaping ([Gillespie2001][tau_leaping] also see [Wikipedia][tau_leaping_wiki])
| | | `ssa.otl` | `tau_adaptive` | Tau leaping with efficient step size selection ([Cao. et al. 2006][tau_adaptive])
BioSimulator.jl | Julia | `Direct` | `direct` |  Gillespie's Direct method ([Gillespie1973][direct])
| | | `TauLeapingDGLP2003` | `tau_leaping` | Improved leap-size selection for accelerated stochastic simulation ([Gillespie and Petzold 2003][dglp2003])
| | | `HybridSAL` | `tau_adaptive` | Step anticipation tau-leaping (SAL) algorithm that defaults to `Direct` depending on cumulative density ([Sehl et. al 2009][hybridsal])

[direct]: https://doi.org/10.1016/0021-9991(76)90041-3
[tau_leaping_wiki]: https://en.wikipedia.org/wiki/Tau-leaping
[tau_leaping]:  https://doi.org/10.1063/1.1378322
[tau_adaptive]: https://doi.org/10.1063%2F1.2159468
[dglp2003]: https://doi.org/10.1063/1.1613254
[hybridsal]: https://dx.doi.org/10.1089/cmb.2008.0249

## Accuracy comparison

To compare the accuracies of the algorithms, we used a subset of the models recommended in the [SBML test suite's stochastic component][sbmltestsuite]. They consist of 4 systems with different parameter combinations, resulting in a total of 14 models or 14 system-parameter combinations.

- For the exact solvers (labeled `direct` in our table above), we used the Z and Y statistics mentioned in the [SBML test suite][sbmltestsuite].
- For the approximate solvers (labeled `tau_leaping` and `tau_adaptive` in our table above), we checked the ratio of means and standard deviations.
- We used 10000 repetitions for each model, for a given library and algorithm.

These decisions are in line with what is recommended in the [SBML test suite][sbmltestsuite].

### Interpolating with `pyssa`'s backend

Stochastic simulation algorithms return the states of the model at random time points (e.g. at time points $t=9.6$ and $t=10.2$ seconds). However, the accuracy tests demand values at specific time points (e.g at $t=10$ seconds). To get the values at the time points needed for accuracy tests, we used `pyssa`'s backend which implements this functionality.

While GillespieSSA and Tellurium do not interpolate in their backends to provide values at specific time points, BioSimulator does possess this functionality. To investigate the effect of different interpolation techniques, we compared BioSimulator's internal interpolation with the raw BioSimulator results interpolated in `pyssa`. We call the former `BioSimulatorIntp` (results are interpolated within `BioSimulator.jl`) in our discussion.

[sbmltestsuite]: https://github.com/sbmlteam/sbml-test-suite/blob/master/cases/stochastic/DSMTS-userguide-31v2.pdf

## Speed comparison

To compare the speed of the different algorithms, we used a subset of models (5 of the 14) used for the accuracy comparisons. These were picked to represent the general breadth of models, with at least one coming from each of the 4 different systems.

- A given model, for a given algorithm from a library, was run 10000 times and the time taken was noted.
- This was repeated 7 times, to get an idea of the variance in the simulation time.
- All simulations were run on single cores.
- Speed was calculated as the inverse of the time taken in seconds for the algorithm to run to completion.

# Results

Here we present some example results from our analysis, followed by key take-homes. The details are presented in the notebook available in the notebooks folder above.

## Example results from comparisons

![image info](./assets/acc_speed_comparison_example.png)

### Accuracy vs. speed

The plot above shows accuracy on the X axis and speed on the Y axis, for one of the 5 models used in the speed comparison. Good algorithms belong on the top right corner of the plot.

- It appears that the direct algorithms (circles) are usually more accurate than the approximate algorithms (crosses and squares).
- The speed of the direct algorithms is not very different from the approximate algorithms. Interestingly, in some cases the direct algorithm is faster than its approximate counterparts.
- Library-wise, we see the following trends:
  - `BioSimulator.jl`'s approximate algorithms are inaccurate.
  - `GillespieSSA` is accurate but slow.
  - The naive `tau_leaping` implemented in `pyssa` is both fast and accurate.

Yet this comparison is limited because it only explores a single model. A comparison of accuracy for different models, followed by speed for different models are presented below.

### Accuracy

### Speed

## Main take homes

# What algorithm should you use?

# Code in this repository
