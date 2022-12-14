# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 15:07:34 2022

@author: stevenweisberg

This script will take as input the run_dsp.py output and return the merged strategy data. 

"""

import pandas as pd

import numpy as np
import os
import glob

# A few wonky participant numbers for dspfmri.
# replacements = {"12002_2":"12002", 210012:"21001", "21002_2":"21002"}


def merge_dsp_data(indir, meta, outdir, excluded=[], replacements={}):

    # We merge three datasets here. One is the trajectories data, providing strategies.
    # The second is success_dfs, which provide whether the trial was completed or not.
    # The third is meta_data, which gives info about which DSP version was which, and when the shortcut intervention was administered.

    # Excluded subjects

    # Where are the data
    traj_dir = os.path.join(indir, "trajectories")
    success_dir = os.path.join(indir, "summary_dfs")

    meta_df = pd.read_csv(meta)

    ## Load in success rates.
    input_files = glob.glob(os.path.join(success_dir, "*.csv"))

    success_df = pd.DataFrame()

    # For each file, we concatenate, but also want to grab the session number from the file name.
    for i in range(len(input_files)):
        with open(input_files[i], "r") as f:
            data = pd.read_csv(input_files[i], sep=",")
        if input_files[i].split("\\")[-1].split("_")[2] == "1":
            data["session"] = "1"
        elif input_files[i].split("\\")[-1].split("_")[2] == "2":
            data["session"] = "2"
        else:
            data["session"] = "1"

        if data.loc[0, "ParticipantNo"] not in excluded:
            success_df = pd.concat([success_df, data])

    success_df["success"] = np.where(success_df["Status"] == "Success", 1, 0)

    success_df["ParticipantNo"].replace(replacements, inplace=True)

    # Groupby a few key variables.
    def f(df):
        d = {}
        d["success"] = df["success"].sum()
        d["distance"] = df["Distance"].mean()
        d["time_elapsed"] = df["Time Elapsed"].mean()
        d["dsp_type"] = df["DSPType"].iloc[0]
        d["total_trials"] = df["DSPType"].count()
        d["session"] = df["session"].iloc[0]
        return pd.Series(
            d,
            index=[
                "success",
                "distance",
                "time_elapsed",
                "dsp_type",
                "total_trials",
                "session",
            ],
        )

    success_wide = success_df.groupby(
        ["ParticipantNo", "DSPType"], as_index=False
    ).apply(f)

    # Make sure no one has duplicated data.
    success_wide = success_wide[success_wide["total_trials"] < 40]

    # Merge with the meta-data
    success_wide = success_wide.merge(
        meta_df, left_on="ParticipantNo", right_on="participant_id"
    )

    ## Trajectories data
    # Load in processed trajectories data
    traj_df = pd.read_csv(os.path.join(traj_dir, "frechet_by_trial.csv"))

    # Wonky subjects.
    traj_df["subject"].replace(replacements, inplace=True)

    # Remove topological strategy
    traj_df.drop(["Top"], axis=1, inplace=True)

    traj_long = pd.melt(
        traj_df.reset_index(),
        id_vars=["subject"],
        value_vars=["Sur", "Rte", "Rev"],
        var_name="strategy",
        value_name="distance",
    )

    df_sub = traj_df[["Rte", "Rev", "Sur"]]
    idx = df_sub.eq(df_sub.min(axis=1), axis=0)
    traj_df["strategy"] = np.where(
        df_sub.eq(df_sub.min(1), 0).sum(1) > 1, "tie", df_sub.idxmin(1)
    )

    # Pivot and get trial counts
    traj_strats_long = (
        traj_df.groupby(["subject", "strategy", "dspVersion"])
        .agg({"Sur": "count"})
        .reset_index()
    )  # Determine whether there are ties or not

    traj_strats_long.rename(columns={"Sur": "trial_counts"}, inplace=True)

    traj_wide = traj_strats_long.pivot(
        index=["subject", "dspVersion"], columns="strategy", values="trial_counts"
    ).reset_index()
    traj_wide.fillna(0, inplace=True)

    # Assemble place_response_index
    traj_wide["route_all"] = traj_wide["Rev"] + traj_wide["Rte"]  # + wide['Rte,Rev']

    traj_wide["place_resp_index"] = traj_wide["Sur"] / (
        traj_wide["Sur"] + traj_wide["route_all"]
    )

    # Merge all data
    all_df = success_wide.merge(
        traj_wide,
        left_on=["ParticipantNo", "DSPType"],
        right_on=["subject", "dspVersion"],
    )

    all_df.to_csv(os.path.join(outdir, "dsp_merged.csv"))
