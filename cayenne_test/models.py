"""
    Common configuration for all the tests
"""

import csv
import pathlib
import numpy as np
from cayenne.utils import Na


def setup_00001():
    """
        Setup the accuracy test 00001.

        Notes
        -----
        A --> A + A; k = 0.1
        A --> _; k = 0.11

        A0 = 100, max_t = 51, max_iter = 1.5e3
    """
    species_names = ["A"]
    rxn_names = ["r1", "r2"]
    V_r = np.array([[1, 1]])
    V_p = np.array([[2, 0]])
    X0 = np.array([100], dtype=np.int64)
    k = np.array([0.1, 0.11])
    max_t = 51
    max_iter = int(1.5e3)
    n_rep = 10
    return (species_names, rxn_names, V_r, V_p, X0, k, max_t, max_iter, n_rep)


def setup_00003():
    """
        Setup the accuracy test 00003.

        Notes
        -----
        A --> A + A; k = 1.0
        A --> _; k = 1.1

        A0 = 100, max_t = 51, max_iter = 1e5
    """
    species_names = ["A"]
    rxn_names = ["r1", "r2"]
    V_r = np.array([[1, 1]])
    V_p = np.array([[2, 0]])
    X0 = np.array([100], dtype=np.int64)
    k = np.array([1.0, 1.1])
    max_t = 51
    max_iter = int(1e5)
    n_rep = 10
    return (species_names, rxn_names, V_r, V_p, X0, k, max_t, max_iter, n_rep)


def setup_00004():
    """
        Setup the accuracy test 00004.

        Notes
        -----
        A --> A + A; k = 0.1
        A --> _; k = 0.11

        A0 = 10, max_t = 51, max_iter = 1.5e3
    """
    species_names = ["A"]
    rxn_names = ["r1", "r2"]
    V_r = np.array([[1, 1]])
    V_p = np.array([[2, 0]])
    X0 = np.array([10], dtype=np.int64)
    k = np.array([0.1, 0.11])
    max_t = 51
    max_iter = int(1.5e3)
    n_rep = 10
    return (species_names, rxn_names, V_r, V_p, X0, k, max_t, max_iter, n_rep)


def setup_00005():
    """
        Setup the accuracy test 00005.

        Notes
        -----
        A --> A + A; k = 0.1
        A --> _; k = 0.11

        A0 = 10_000, max_t = 51, max_iter = 5e5
    """
    species_names = ["A"]
    rxn_names = ["r1", "r2"]
    V_r = np.array([[1, 1]])
    V_p = np.array([[2, 0]])
    X0 = np.array([10_000], dtype=np.int64)
    k = np.array([0.1, 0.11])
    max_t = 51
    max_iter = int(5e5)
    n_rep = 10
    return (species_names, rxn_names, V_r, V_p, X0, k, max_t, max_iter, n_rep)


def setup_00011():
    """
        Setup the accuracy test 00011.

        Notes
        -----
        A --> A + A; k = 0.1/2
        A --> _; k = 0.11/2

        A0 = 100, max_t = 51, max_iter = 1.5e3
    """
    species_names = ["A"]
    rxn_names = ["r1", "r2"]
    V_r = np.array([[1, 1]])
    V_p = np.array([[2, 0]])
    X0 = np.array([100], dtype=np.int64)
    # divide k by 2 because rate expression given in units of concentration
    # in the model file
    k = np.array([0.1, 0.11]) / 2
    max_t = 51
    max_iter = int(1.5e3)
    n_rep = 10
    return (species_names, rxn_names, V_r, V_p, X0, k, max_t, max_iter, n_rep)


def setup_00020():
    """
        Setup the accuracy test 00020.

        Notes
        -----
        _ --> A; k = 1
        A --> _; k = 0.1

        A0 = 0, max_t = 52, max_iter = 1.5e3
    """
    species_names = ["A"]
    rxn_names = ["r1", "r2"]
    V_r = np.array([[0, 1]])
    V_p = np.array([[1, 0]])
    X0 = np.array([0], dtype=np.int64)
    k = np.array([1.0, 0.1])
    max_t = 52
    # we did 52 because direct would stop earlier than 50, but we want at least 50 crossed.
    max_iter = int(1.5e3)
    n_rep = 10
    return (species_names, rxn_names, V_r, V_p, X0, k, max_t, max_iter, n_rep)


def setup_00021():
    """
        Setup the accuracy test 00021.

        Notes
        -----
        _ --> A; k = 10.0
        A --> _; k = 0.1

        A0 = 0, max_t = 51, max_iter = 1.5e3
    """
    species_names = ["A"]
    rxn_names = ["r1", "r2"]
    V_r = np.array([[0, 1]])
    V_p = np.array([[1, 0]])
    X0 = np.array([0], dtype=np.int64)
    k = np.array([10.0, 0.1])
    max_t = 51
    max_iter = int(1.5e3)
    n_rep = 10
    return (species_names, rxn_names, V_r, V_p, X0, k, max_t, max_iter, n_rep)


def setup_00022():
    """
        Setup the accuracy test 00022.

        Notes
        -----
        _ --> A; k = 5.0
        A --> _; k = 0.1

        A0 = 0, max_t = 51, max_iter = 1.5e3
    """
    species_names = ["A"]
    rxn_names = ["r1", "r2"]
    V_r = np.array([[0, 1]])
    V_p = np.array([[1, 0]])
    X0 = np.array([0], dtype=np.int64)
    k = np.array([5.0, 0.1])
    max_t = 51
    max_iter = int(1.5e3)
    n_rep = 10
    return (species_names, rxn_names, V_r, V_p, X0, k, max_t, max_iter, n_rep)


def setup_00023():
    """
        Setup the accuracy test 00023.

        Notes
        -----
        _ --> A; k = 1000
        A --> _; k = 0.1

        A0 = 0, max_t = 51, max_iter = 1.5e5
    """
    species_names = ["A"]
    rxn_names = ["r1", "r2"]
    V_r = np.array([[0, 1]])
    V_p = np.array([[1, 0]])
    X0 = np.array([0], dtype=np.int64)
    k = np.array([1000.0, 0.1])
    max_t = 51
    max_iter = int(1.5e5)
    n_rep = 10
    return (species_names, rxn_names, V_r, V_p, X0, k, max_t, max_iter, n_rep)


def setup_00030():
    """
        Setup the accuracy test 00030.

        Notes
        -----
        A + A --> A2; k = 0.001
        A2 --> A + A; k = 0.01

        A0 = 100, max_t = 55, max_iter = 1.5e5

        In the model description, they just say k1 = 0.001 without specifying
        deterministic or stochastic. They end up using k1_stoc = 0.001. To have
        k1_stoc = 0.001, we should set k1_det = 0.001/2.
    """
    species_names = ["A", "A2"]
    rxn_names = ["r1", "r2"]
    V_r = np.array([[2, 0], [0, 1]])
    V_p = np.array([[0, 2], [1, 0]])
    X0 = np.array([100, 0], dtype=np.int64)
    k = np.array([0.001 / 2, 0.01])
    max_t = 55
    max_iter = int(1.5e5)
    n_rep = 10
    return (species_names, rxn_names, V_r, V_p, X0, k, max_t, max_iter, n_rep)


def setup_00031():
    """
        Setup the accuracy test 00031.

        Notes
        -----
        A + A --> A2; k = 0.0002
        A2 --> A + A; k = 0.004

        A0 = 1000, max_t = 52, max_iter = 1.5e5

        In the model description, they just say k1 = 0.0002 without specifying
        deterministic or stochastic. They end up using k1_stoc = 0.0002. To
        have k1_stoc = 0.0002, we should set k1_det = 0.0002/2.
    """
    species_names = ["A", "A2"]
    rxn_names = ["r1", "r2"]
    V_r = np.array([[2, 0], [0, 1]])
    V_p = np.array([[0, 2], [1, 0]])
    X0 = np.array([1000, 0], dtype=np.int64)
    k = np.array([0.0002 / 2, 0.004])
    max_t = 52
    max_iter = int(1.5e5)
    n_rep = 20
    return (species_names, rxn_names, V_r, V_p, X0, k, max_t, max_iter, n_rep)


def setup_00037():
    """
        Setup the accuracy test 00037.

        Notes
        -----
        _ --> 5A; k = 1.0
        A --> _; k = 0.2

        A0 = 0, max_t = 53, max_iter = 1.5e3
    """
    species_names = ["A"]
    rxn_names = ["r1", "r2"]
    V_r = np.array([[0, 1]])
    V_p = np.array([[5, 0]])
    X0 = np.array([0], dtype=np.int64)
    k = np.array([1.0, 0.2])
    max_t = 53
    max_iter = int(1.5e3)
    n_rep = 10
    return (species_names, rxn_names, V_r, V_p, X0, k, max_t, max_iter, n_rep)


def setup_00038():
    """
        Setup the accuracy test 00038.

        Notes
        -----
        _ --> 10A; k = 1.0
        A --> _; k = 0.2

        A0 = 0, max_t = 53, max_iter = 1.5e3

        In the model description, they just say k2 = 0.2 without specifying
        deterministic or stochastic. This is a first order reaction, so
        technically k2 = k2_stoc. They instead use kstoc = 0.4 in the model
        file, so this value is used.
    """
    species_names = ["A"]
    rxn_names = ["r1", "r2"]
    V_r = np.array([[0, 1]])
    V_p = np.array([[10, 0]])
    X0 = np.array([0], dtype=np.int64)
    k = np.array([1.0, 0.4])
    max_t = 53
    max_iter = int(1.5e3)
    n_rep = 10
    return (species_names, rxn_names, V_r, V_p, X0, k, max_t, max_iter, n_rep)


def setup_00039():
    """
        Setup the accuracy test 00038.

        Notes
        -----
        _ --> 10A; k = 1.0
        A --> _; k = 0.2

        A0 = 0, max_t = 53, max_iter = 1.5e5

        In the model description, they just say k2 = 0.2 without specifying
        deterministic or stochastic. This is a first order reaction, so
        technically k2 = k2_stoc. They instead use kstoc = 4.0 in the model
        file, so this value is used.
    """
    species_names = ["A"]
    rxn_names = ["r1", "r2"]
    V_r = np.array([[0, 1]])
    V_p = np.array([[100, 0]])
    X0 = np.array([0], dtype=np.int64)
    k = np.array([1.0, 4.0])
    max_t = 53
    max_iter = int(1.5e5)
    n_rep = 10
    return (species_names, rxn_names, V_r, V_p, X0, k, max_t, max_iter, n_rep)


def get_model(model_id):
    """ Returns model given model_id """
    model_name = "setup_" + model_id
    return globals()[model_name]()
