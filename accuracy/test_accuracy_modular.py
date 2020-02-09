import sys
from helpers import calculate_zy, read_results, process_r
from helpers import read_results_2sp, calculate_zy_2sp, process_r_2sp
import numpy as np


id_ = sys.argv[1]
library = sys.argv[2]
algo = sys.argv[3]

two_species_models = ["00030"]

if id_ not in two_species_models:
    time_list, mu_list, std_list = read_results(id_)
    res = process_r(id_, library=library, algo=algo)
    Z, Y = calculate_zy(res, time_list, mu_list, std_list)
else:
    print("Using 2 species")
    time_list, mu_list, std_list = read_results_2sp(id_)
    res = process_r_2sp(id_, library=library, algo=algo)
    Z, Y = calculate_zy_2sp(res, time_list, mu_list, std_list)
# print(res.get_state(1.0))
assert (-3 < Z).all()
try:
    assert (Z < 3).all()
except AssertionError:
    print(np.where(Z < 3))
assert (-5 < Y).all()
assert (Y < 5).all()
