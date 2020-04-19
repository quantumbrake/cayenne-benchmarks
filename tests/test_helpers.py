import numpy as np

from accuracy.helpers import (
    read_results_analytical,
    read_results_analytical_2sp,
    get_highest_rep_in_path,
    read_results_simulation,
    read_results_simulation_2sp,
    calculate_zy,
    calculate_zy_2sp,
    calculate_ms_ratios
)


def test_rr_analytical():
    time, mu, std = read_results_analytical("00001")
    nrow = time.shape[0]
    assert nrow == 51
    assert mu.shape[0] == nrow
    assert std.shape[0] == nrow


def test_rr_analytical_2sp():
    time, mu, std = read_results_analytical_2sp("00030")
    nrow = time.shape[0]
    assert nrow == 51
    assert mu.shape[0] == nrow
    assert std.shape[0] == nrow
    assert mu.shape[1] == 2
    assert mu.shape[1] == 2


def test_highest_rep_in_path():
    assert get_highest_rep_in_path("./tests/data/1sp/") == 5


def test_rr_simulation():
    res = read_results_simulation(n_reps=5, res_folder="tests/data/1sp/")
    assert len(res) == 5
    assert (res.t_list[0] == [0, 1, 2, 3, 4]).all()
    assert (res.t_list[3] == [0, 1]).all()
    res = read_results_simulation(n_reps=3, res_folder="tests/data/1sp/")
    assert len(res) == 3


def test_calculate_zy():
    res = read_results_simulation(n_reps=3, res_folder="tests/data/1sp/", algo="direct")
    time_arr = [0, 1, 2, 3, 4]
    mu_analytical = [0, 1, 2, 3, 4]
    std_manual = np.std([0, 1, 2])
    std_analytical = [0, std_manual, std_manual, std_manual, std_manual]
    z, y, mu_obs, std_obs = calculate_zy(
        res, time_arr, mu_analytical, std_analytical, True
    )
    assert len(z) == len(time_arr) - 1
    assert len(y) == len(time_arr) - 1
    assert np.isclose(mu_obs, mu_analytical).all()
    assert np.isclose(std_obs, std_analytical).all()
    assert np.isclose(z, [0, 0, 0, 0]).all()
    assert np.isclose(y, [0, 0, 0, 0]).all()

    z, y, mu_obs, std_obs = calculate_zy(
        res, time_arr, mu_analytical, std_analytical, False
    )
    assert len(z) == len(time_arr) - 1
    assert len(y) == len(time_arr) - 1
    assert np.isclose(mu_obs, mu_analytical).all()
    assert np.isclose(std_obs, std_analytical).all()
    assert np.isclose(z, [0, 0, 0, 0]).all()
    assert np.isclose(y, [0, 0, 0, 0]).all()

    res = read_results_simulation(
        n_reps=3, res_folder="tests/data/1sp/", algo="not_direct"
    )

    z, y, mu_obs, std_obs = calculate_zy(
        res, time_arr, mu_analytical, std_analytical, False
    )
    assert len(z) == len(time_arr) - 1
    assert len(y) == len(time_arr) - 1
    assert np.isclose(mu_obs, mu_analytical).all()
    assert np.isclose(std_obs, std_analytical).all()
    assert np.isclose(z, [0, 0, 0, 0]).all()
    assert np.isclose(y, [0, 0, 0, 0]).all()


def test_rr_simulation_2sp():
    res = read_results_simulation_2sp(n_reps=4, res_folder="tests/data/2sp/")
    assert len(res) == 4
    assert (res.t_list[0] == [0, 1, 2, 3, 4]).all()
    assert (res.t_list[3] == [0, 1]).all()
    assert (res.x_list[3] == np.array([[0, 10], [1, 9]])).all()
    res = read_results_simulation_2sp(n_reps=3, res_folder="tests/data/2sp/")
    assert len(res) == 3


def test_calculate_zy_2sp():
    # time, mu, std = read_results_analytical("00001")
    res = read_results_simulation_2sp(
        n_reps=3, res_folder="tests/data/2sp/", algo="direct"
    )

    time_arr = [0, 1, 2, 3, 4]
    mu_analytical = np.array([[0, 10], [1, 9], [2, 8], [3, 7], [4, 6]])
    std_manual = np.std([1, 2, 3])
    std_analytical = np.array(
        [
            [0, 0],
            [std_manual, std_manual],
            [std_manual, std_manual],
            [std_manual, std_manual],
            [std_manual, std_manual],
        ]
    )

    z, y, mu_obs, std_obs = calculate_zy_2sp(
        res, time_arr, mu_analytical, std_analytical, True
    )
    assert len(z) == len(time_arr) - 1
    assert len(y) == len(time_arr) - 1
    assert np.isclose(mu_obs, mu_analytical).all()
    assert np.isclose(std_obs, std_analytical).all()
    assert np.isclose(z, np.array([[0, 0, 0, 0], [0, 0, 0, 0]]).transpose()).all()
    assert np.isclose(y, np.array([[0, 0, 0, 0], [0, 0, 0, 0]]).transpose()).all()

    z, y, mu_obs, std_obs = calculate_zy_2sp(
        res, time_arr, mu_analytical, std_analytical, False
    )
    assert len(z) == len(time_arr) - 1
    assert len(y) == len(time_arr) - 1
    assert np.isclose(mu_obs, mu_analytical).all()
    assert np.isclose(std_obs, std_analytical).all()
    assert np.isclose(z, np.array([[0, 0, 0, 0], [0, 0, 0, 0]]).transpose()).all()
    assert np.isclose(y, np.array([[0, 0, 0, 0], [0, 0, 0, 0]]).transpose()).all()

    res = read_results_simulation_2sp(
        n_reps=3, res_folder="tests/data/2sp/", algo="not_direct"
    )

    z, y, mu_obs, std_obs = calculate_zy_2sp(
        res, time_arr, mu_analytical, std_analytical, False
    )
    assert len(z) == len(time_arr) - 1
    assert len(y) == len(time_arr) - 1
    assert np.isclose(mu_obs, mu_analytical).all()
    assert np.isclose(std_obs, std_analytical).all()
    assert np.isclose(z, np.array([[0, 0, 0, 0], [0, 0, 0, 0]]).transpose()).all()
    assert np.isclose(y, np.array([[0, 0, 0, 0], [0, 0, 0, 0]]).transpose()).all()


def test_ms_ratios():
    # test 1d and 2d in the same call
    mu_obs = np.array([1, 2, 3])
    mu_analytical = np.array([2, 8, 15])
    # make std floats since we expect them to be
    std_obs = np.array([[2.0, 4, 6, 8], [5, 12, 14, 16]])
    # include a 0. ratio will be inf, but that should be caught and set to 1.
    std_analytical = np.array([[1, 2, 3, 4], [0, 6, 7, 8]])
    mu_ratio, std_ratio = calculate_ms_ratios(
        mu_obs=mu_obs,
        mu_analytical=mu_analytical,
        std_obs=std_obs,
        std_analytical=std_analytical,
    )
    expected_mu_ratio = np.array([1 / 2.0, 1 / 4.0, 1 / 5.0])
    expected_std_ratio = np.array([[2, 2, 2, 2], [1, 2, 2, 2]])
    assert np.isclose(mu_ratio, expected_mu_ratio).all()
    assert np.isclose(std_ratio, expected_std_ratio).all()
