#!/usr/bin/env python3

import json
import matplotlib.pyplot as plt
import pathlib

import numpy as np
import pandas as pd
import seaborn as sns

PALETTE_5 = sns.color_palette("Set2", n_colors=5)
LIB_PALETTE = {
    "Cayenne": PALETTE_5[0],
    "BioSimulator-CI": PALETTE_5[1],
    "BioSimulator": PALETTE_5[2],
    "GillespieSSA": PALETTE_5[3],
    "Tellurium": PALETTE_5[4],
}
PALETTE_3 = sns.color_palette("Set2", n_colors=3)
ALGO_PALETTE = {
    "direct": PALETTE_3[0],
    "tau_leaping": PALETTE_3[1],
    "tau_adaptive": PALETTE_3[2],
}

MODEL_ORDER = [
    "001-01",
    "001-03",
    "001-04",
    "001-05",
    "001-11",
    "002-01",
    "002-02",
    "002-03",
    "002-04",
    "003-01",
    "003-02",
    "004-01",
    "004-02",
    "004-03",
]
MODELID_NAME_DICT = {
    "00001": "001-01",
    "00003": "001-03",
    "00004": "001-04",
    "00005": "001-05",
    "00011": "001-11",
    "00020": "002-01",
    "00021": "002-02",
    "00022": "002-03",
    "00023": "002-04",
    "00030": "003-01",
    "00031": "003-02",
    "00037": "004-01",
    "00038": "004-02",
    "00039": "004-03",
}
LIBID_NAME_DICT = {
    "BioSimulator": "BioSimulator-CI",
    "BioSimulatorIntp": "BioSimulator",
    "cayenne": "Cayenne",
}


def make_accuracy_df(filename: str, use_ratio_for_approx=True):
    """ Compile all accuracy results into a pandas dataframe """
    full_algos = ["direct"]
    approx_algos = ["tau_leaping", "tau_adaptive"]
    df = pd.read_csv(filename, dtype={"model": str})
    df.replace({"model": MODELID_NAME_DICT}, inplace=True)
    df.replace({"lib": LIBID_NAME_DICT}, inplace=True)
    df.loc[:, "nspecies"] = 1
    df.loc[df.model.isin(["003-01", "003-02"]), "nspecies"] = 2
    df.loc[:, "ntest"] = df.nspecies * 100  # number of tests
    # Number passing should be ntest
    full_inds = df.algo.isin(full_algos)
    approx_inds = df.algo.isin(approx_algos)
    if use_ratio_for_approx:
        df.loc[full_inds, "total_pass"] = (
            (
                df[full_inds].ntest
                - (
                    df.loc[full_inds, "test0"]
                    + df.loc[full_inds, "test1"]
                    + df.loc[full_inds, "test2"]
                    + df.loc[full_inds, "test3"]
                )
            )
            / df[full_inds].ntest
            * 100
        )

        df.loc[approx_inds, "total_pass"] = (
            (
                df[approx_inds].ntest
                - (
                    df.loc[approx_inds, "rtest0"]
                    + df.loc[approx_inds, "rtest1"]
                    + df.loc[approx_inds, "rtest2"]
                    + df.loc[approx_inds, "rtest3"]
                )
            )
            / df[approx_inds].ntest
            * 100
        )
    else:
        df.loc[:, "total_pass"] = (
            (df.ntest - (df["test0"] + df["test1"] + df["test2"] + df["test3"]))
            / df.ntest
            * 100
        )
    # If test0 is -1 because test didn't ocmplete, then they should be labeled as such.
    df.loc[df["total_pass"] > df.ntest, "total_pass"] = -0.1
    return df


def make_benchmark_df(path):
    """ Compile all benchmark results into a pandas dataframe """
    files = list(pathlib.Path(path).glob("*.json"))
    results = []
    for this_file in files:
        with open(this_file) as fid:
            data_dict = json.load(fid)
            lib, algo, model, nreps = this_file.stem.split("-")
            this_result = data_dict["results"][0]
            this_result["lib"] = lib
            this_result["algo"] = algo
            this_result["model"] = model
            this_result["nrep"] = int(nreps)
            results.append(this_result)
    df = pd.DataFrame(results)
    df.replace({"model": MODELID_NAME_DICT}, inplace=True)
    df.replace({"lib": LIBID_NAME_DICT}, inplace=True)
    df = df[df.nrep == 10000]
    return df


def plot_accuracy_barplot(df, hue="algo"):
    """ Plot a barplot of total success for each test in the df """
    plt.figure(figsize=(14, 5))
    if hue == "lib":
        current_palette = sns.color_palette("Set1", n_colors=5)
        libs = set(df["lib"])
        new_palette = {key: value for key, value in LIB_PALETTE.items() if key in libs}
        g = sns.barplot(
            x="model",
            y="total_pass",
            hue=hue,
            data=df,
            palette=new_palette,
            order=MODEL_ORDER,
            hue_order=reversed(sorted(new_palette.keys())),
        )
    elif hue == "algo":
        current_palette = sns.color_palette("Set1", n_colors=3)
        algos = set(df["algo"])
        new_palette = {
            key: value for key, value in ALGO_PALETTE.items() if key in algos
        }
        g = sns.barplot(
            x="model",
            y="total_pass",
            hue=hue,
            data=df,
            palette=new_palette,
            order=MODEL_ORDER,
            hue_order=reversed(sorted(new_palette.keys())),
        )
    else:
        g = sns.barplot(x="model", y="total_pass", hue=hue, data=df, order=MODEL_ORDER)
    two_sp_models = ["003-01", "003-02"]
    for p in g.patches:
        if np.isnan(p.get_height()):
            continue
        if p.get_height() < 0:
            color = "blue"
            height = "dnf"
        else:
            height = int(p.get_height())
            if height == 100:
                color = "green"
            else:
                color = "red"
        g.annotate(
            f"{height}",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=8,
            color=color,
            xytext=(0, 10),
            textcoords="offset points",
            rotation=45,
        )
    plt.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.05),
        ncol=5,
        fancybox=True,
        framealpha=1.0,
        # shadow=True,
    )
    plt.ylabel("Accuracy score")
    plt.xlabel("Model")
    plt.ylim(-5, 120)


def plot_benchmark_barplot(df):
    """ Plot a barplot of time taken for each simulation in the df """
    times = df.explode("times")
    sns.barplot(x="model", y="times", hue="lib", data=times)
