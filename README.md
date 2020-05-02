# Goal

The goal of this repository is to compare the different softwares used for stochastic / Gillespie type simulations (see [Wikipedia](https://en.wikipedia.org/wiki/Gillespie_algorithm)). These simulations are used to model biological processes or chemical reactions when the corresponding differential equations cannot be applied. This may be the case when the number of species being modeled is very small (such as 10s of molecules/biological spcies), and the randomness becomes important. A simple example is a starting with a small number of bacteria (say 5) in a dish. They may either all die out, or they may start dividing and growing rapidly. The outcome itself is random, and you would use a Gillespie simulator to model such a process.


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
| | | `TauLeapingDGLP2003()` | `tau_leaping` | Improved leap-size selection for accelerated stochastic simulation ([Gillespie and Petzold 2003][dglp2003])
| | | `HybridSAL()` | `tau_adaptive` | Step anticipation tau-leaping (SAL) algorithm that defaults to `Direct` depending on cumulative density ([Sehl et. al 2009][hybridsal])

[direct]: https://doi.org/10.1016/0021-9991(76)90041-3
[tau_leaping_wiki]: https://en.wikipedia.org/wiki/Tau-leaping
[tau_leaping]:  https://doi.org/10.1063/1.1378322
[tau_adaptive]: https://doi.org/10.1063%2F1.2159468
[dglp2003]: https://doi.org/10.1063/1.1613254
[hybridsal]: https://dx.doi.org/10.1089/cmb.2008.0249

