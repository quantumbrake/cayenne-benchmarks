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
pyssa (v0.9.1) | Python (v3.6.9) | `direct` | `direct` | Gillespie's Direct method ([Gillespie1973][direct])
| | | `tau_leaping` | `tau_leaping` | Standard tau leaping ([Gillespie2001][tau_leaping] also see [Wikipedia][tau_leaping_wiki])
| | | `tau_adaptive` | `tau_adaptive` | Tau leaping with efficient step size selection ([Cao. et al. 2006][tau_adaptive])
Tellurium (v2.1.5) | Python (v3.6.9) | `gillespie` | `direct` | Unknown (see [here](https://tellurium.readthedocs.io/en/latest/_notebooks/core/tellurium_stochastic.html?highlight=gillespie#stochastic-simulation)), likely similar to Gillespie's Direct Method
GillespieSSA (0.6.1) | R (v3.6.1) | `ssa.d` | `direct` | Gillespie's Direct method ([Gillespie1973][direct])
| | | `ssa.etl` | `tau_leaping` |  Standard tau leaping ([Gillespie2001][tau_leaping] also see [Wikipedia][tau_leaping_wiki])
| | | `ssa.otl` | `tau_adaptive` | Tau leaping with efficient step size selection ([Cao. et al. 2006][tau_adaptive])
BioSimulator.jl (v0.9.3)| Julia (v1.4.0) | `Direct` | `direct` |  Gillespie's Direct method ([Gillespie1973][direct])
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

- The direct algorithm was generally accurate across the packages tested. The exceptions are
  - `BioSimulator.jl` appears to interpolate values poorly. When BioSimulator's raw results were interpolated with `pyssa`'s backend, the accuracy was restored.
  - `Tellurium`'s appears to be inaccurate when reactions are second order (usually occurs when there are two reactants).
- The approximate algorithms on average performed poorly compared to their direct counterparts across different models. Some systemic bugs/defects we identified are:
  - `BioSimulator.jl` and `GillespieSSA` fail to simulate the system if the number of molecules is initially zero. They don't account for zero order reactions which can result in valid simulations, such as migration into the system.

### Speed

- `pyssa`, `BioSimulator` and `Tellurium` were similar in speed.
- `GillespieSSA` was at least an order of magnitude slower than the rest of the packages. This was observed across different models and algorithms.

# What algorithm should you use?

<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-style:solid;border-width:0px;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;
  padding:10px 5px;word-break:normal;}
.tg th{border-style:solid;border-width:0px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-0lax{text-align:left;vertical-align:top}
.tg .tg-green{background-color:#c6e0b4;border-color:#000000;text-align:left;vertical-align:top}
.tg .tg-orange{background-color:#ffe685;border-color:#000000;text-align:left;vertical-align:top}
.tg .tg-73oq{border-color:#000000;text-align:left;vertical-align:top}
.tg .tg-red{background-color:#f4b084;border-color:#000000;text-align:left;vertical-align:top}
</style>
<table class="tg">
<thead>
  <tr>
    <th class="tg-0lax"></th>
    <th class="tg-0lax">direct</th>
    <th class="tg-0lax">tau_leaping</th>
    <th class="tg-0lax">tau_adaptive</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-0lax">pyssa</td>
    <td class="tg-green">Most   accurate yet</td>
    <td class="tg-green">Very fast but may need manual tuning</td>
    <td class="tg-orange">Less   accurate than GillespieSSA's version</td>
  </tr>
  <tr>
    <td class="tg-0lax">Tellurium</td>
    <td class="tg-orange">Inaccurate   for 2nd order</td>
    <td class="tg-73oq">N/A</td>
    <td class="tg-73oq">N/A</td>
  </tr>
  <tr>
    <td class="tg-0lax">GillespieSSA</td>
    <td class="tg-orange">Very   slow</td>
    <td class="tg-red">Inaccurate   for initial zero counts</td>
    <td class="tg-red">Inaccurate   for initial zero counts</td>
  </tr>
  <tr>
    <td class="tg-0lax">BioSimulator.jl</td>
    <td class="tg-orange">Inaccurate   interpolation</td>
    <td class="tg-red">Inaccurate   for initial zero counts</td>
    <td class="tg-red">Inaccurate   for initial zero counts</td>
  </tr>
</tbody>
</table>

- From this table above, a user is best off starting with `pyssa`'s `direct` algorithm. It is accurate for several different model configurations.
- If `direct` is too slow, `pyssa`'s `tau_leaping` may be considered. This may require some hand-tuning of the `tau` parameter depending on the system. But we found that fixing the value to `0.1` sufficed for most of the accuracy tests.
- Other algorithms and packages may be considered if the system under consideration does not begin with initial amounts set to zero or if there aren't higher order reactions.

# Code in this repository

