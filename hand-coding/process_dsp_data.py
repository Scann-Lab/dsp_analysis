import os
from shutil import copyfile
import glob
import pandas as pd
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from imageio import imread
import warnings

# Do you want to re-run all subjects?
rerun_all = False

# Turn off interactive plots
plt.ioff()

# Expects that the data is somewhere relative to the Analysis script
scriptDir = os.path.dirname(os.path.realpath(__file__))

# For testing
#indir = os.path.join(scriptDir, "..", "tests")


# Where are the raw data?
indir = os.path.join(scriptDir, "..", "..", "DSP_RawData")

# These should be set relative to the code directory.
outdir_base = os.path.join(indir, "Script_Output_DO_NOT_TOUCH")
outdir_for_summary_dfs = os.path.join(outdir_base, "summary_dfs")
outdir_for_pdfs = os.path.join(outdir_base, "pdfs")
outdir_movement = os.path.join(outdir_base, "raw_movement_data")

os.makedirs(outdir_for_summary_dfs, exist_ok=True)
os.makedirs(outdir_for_pdfs, exist_ok=True)
os.makedirs(outdir_movement, exist_ok=True)

# Select all text files corresponding to test (e.g., NOT listed with Training or Ranking in the filename)
raw_files_all = list(
    set(glob.glob(indir + "//*.txt"))
    - set(glob.glob(indir + "//*Training*"))
    - set(glob.glob(indir + "//*Ranking*"))
)


def calculate_distance(x1, y1, x2, y2):  # simple distance formula
    x = x1 - x2
    y = y1 - y2
    x = x**2
    y = y**2
    z = x + y
    return np.round(np.sqrt(z), 2)


def get_time_elapsed(raw_df):
    """Collect the time to complete each trial"""
    times = []

    # Get the trial ids from raw data, which have the indices.
    # We will use the indices to find the last line of the previous trial.
    # We need to handle the last trial differently
    trial_ids = raw_df.query(
        'lines.str.contains("!!")', engine="python"
    ).drop_duplicates()

    for index, row in trial_ids.iterrows():

        times.append(raw_df.iloc[index - 1]["lines"].split(":")[0])

    # Last trial is the last non-empty row
    times.append(raw_df.dropna().iloc[-1]["lines"].split(":")[0])

    # Remove the first value, which is extraneous (before the first trial)
    times.pop(0)

    # For the rest, we want to convert them to float to handle incomplete trials
    times_float = []

    for x in times:
        try:
            times_float.append(float(x))
        except:
            times_float.append(np.nan)

    return times_float


def get_distance_measures(raw_df):

    trial_ids = raw_df.query(
        'lines.str.contains("!!")', engine="python"
    ).drop_duplicates(keep="last")

    indices = list(trial_ids.index)
    indices.append(raw_df.index[-1] + 1)
    last_index = raw_df.index[-1] + 1

    movement_df_all = pd.DataFrame(
        columns=[
            "ParticipantNo",
            "TrialID",
            "x",
            "z",
            "time",
            "angle",
            "prev_x",
            "prev_z",
        ]
    )

    for i, index in enumerate(indices):
        if index != last_index:

            slice = raw_df.iloc[indices[i] + 1 : indices[i + 1]]

            movement_df = pd.DataFrame(
                columns=["ParticipantNo", "TrialID", "x", "z", "time", "angle"]
            )

            movement_df_all = movement_df_all.append(
                make_movement_data(slice, movement_df, trial_ids.iloc[i]["lines"])
            )

    movement_df_all["dist"] = movement_df_all.apply(
        lambda x: calculate_distance(x["prev_x"], x["prev_z"], x["x"], x["z"]), axis=1
    )

    return movement_df_all


def parse_lines(line):
    t = line[0].split(":  ")[0]
    x = line[0].split(":  ")[1]
    z = line[1]
    angle = line[2]

    return float(t), float(x), float(z), float(angle)


def make_movement_data(slice, movement_df, trial_id):

    if not slice.empty:
        (
            movement_df["time"],
            movement_df["x"],
            movement_df["z"],
            movement_df["angle"],
        ) = zip(*slice["lines"].str.split(",").apply(parse_lines))

        movement_df["prev_x"] = movement_df.x.shift(1)
        movement_df["prev_z"] = movement_df.z.shift(1)

    movement_df["TrialID"] = trial_id.split("_")[-2] + "_" + trial_id.split("_")[-1]

    return movement_df


def pandas_to_csv(raw_df, default_fail_time="40"):

    # Column names
    outputHeader = [
        "ParticipantNo",
        "DSPType",
        "EncodingTours",
        "TrialNo",
        "TrialID",
        "Time Elapsed",
        "Status",
        "FailTime",
    ]

    # Get number of trials based on how many times !! appears (a trial marker in the original script)
    # Note, there is typically one duplicate entry of !!, so we remove that

    trial_ids = list(
        raw_df.query('lines.str.contains("!!")', engine="python").drop_duplicates()[
            "lines"
        ]
    )

    nTrials = len(trial_ids)

    # Initialize the dataframe to store the output data
    df = pd.DataFrame(columns=outputHeader)

    # Trial sequence from 1 to number of trials
    df["TrialNo"] = range(1, nTrials + 1, 1)
    # Participant ID
    df["ParticipantNo"] = (
        raw_df.query('lines.str.contains("ParticipantNo")', engine="python")
        .iloc[0]["lines"]
        .split(": ")[-1]
    )
    # DSP Type (version of the maze. Can be 1 = Normal, 2 = Alternate)
    df["DSPType"] = (
        raw_df.query('lines.str.contains("DSPType")', engine="python")
        .iloc[0]["lines"]
        .split(": ")[-1]
    )
    # Number of laps around the track. 0 means default for the experiment.
    df["EncodingTours"] = (
        raw_df.query('lines.str.contains("Encoding Tours")', engine="python")
        .iloc[0]["lines"]
        .split(": ")[-1]
    )
    # Trial ID number (each trial has a unique 2 digit number from 1-24)
    df["TrialID"] = [x.split("_")[-2] + "_" + x.split("_")[-1] for x in trial_ids]
    # How long participants had until the trial ended
    try:
        df["FailTime"] = (
            raw_df.query('lines.str.contains("Time for")', engine="python")
            .iloc[0]["lines"]
            .split(": ")[-1]
        )
    except:
        df["FailTime"] = default_fail_time

    # Amount of time they took per trial
    df["Time Elapsed"] = get_time_elapsed(raw_df)

    # Whether that trial was a success (they reached the goal in time) or not (failure)
    df["Status"] = np.where(
        df["FailTime"].astype("float") - df["Time Elapsed"].astype("float") > 0.0201,
        "Success",
        "Failure",
    )

    # Get a dataframe where each row is the position and facing direction (and trial ID) for each timepoint
    movement_df = get_distance_measures(raw_df)

    # Based on this, we can calculate distance traveled for each trial.
    distances = movement_df.groupby("TrialID")["dist"].sum()
    distances.name = "Distance"
    df = df.merge(distances, on="TrialID", how="outer")

    # And we can calculate time to first movement
    first_moves = movement_df[movement_df["dist"] > 0.001].drop_duplicates(
        "TrialID", keep="first"
    )[["TrialID", "time"]]
    first_moves = first_moves.rename(columns={"t": "Time_to_First_Movement"})
    df = df.merge(first_moves, on="TrialID", how="outer")

    movement_df["ParticipantNo"] = (
        raw_df.query('lines.str.contains("ParticipantNo")', engine="python")
        .iloc[0]["lines"]
        .split(": ")[-1]
    )

    return df, movement_df


def save_file(df, file: str, dir: str):

    df.to_csv(os.path.abspath(os.path.join(dir, file)), index=False)

    print(f"File saved as: {dir}//{file}\n")


def graph_trial(movement_df, trial_id, pdf):

    trial_df = movement_df[movement_df["TrialID"] == trial_id]

    try:
        assert trial_df["TrialID"].nunique() == 1, f"Trial: {trial_id}"
    except:
        raise ValueError("DataFrame must have only one value for TrialID.")

    plt.figure(dpi=350)
    figureFiletype = ".png"
    plt.plot(trial_df["x"], trial_df["z"], "k", label="__nolegend__")

    v = [0, 222, 0, 222]
    plt.axis(v)
    plt.ylabel("Y")
    plt.xlabel("X")
    plt.title(trial_id)
    plt.legend(["Path"], loc="center left", bbox_to_anchor=(1.0, 0.5))

    # Open the image with that trial structure
    imageFilename = trial_id.upper() + figureFiletype
    bestImage = os.path.join(scriptDir, "..", "Nav_stratAbility_Maps", imageFilename)
    img = imread(bestImage)

    plt.imshow(img, zorder=0, extent=[0.0, 222.0, 0.0, 222.0])  # left right bottom top
    pdf.savefig()
    plt.close()


def select_files(raw_files_all, exclude_dir, movement=False):

    strip = -4 if not movement else -13
    exclude_files = []
    already_coded_stems = []
    already_coded = os.listdir(exclude_dir)
    for i in already_coded:
        if "Participant" in i:
            already_coded_stems.append(i[:strip] + ".txt")
    for i in already_coded_stems:
        exclude_files += [f for f in raw_files_all if i in f]

    raw_files = list(set(raw_files_all) - set(exclude_files))

    return sorted(raw_files)


def run_all(file, csv=True, movement=True, pdf=True):

    # Processing file
    print(f"Processing {file}\n")
    # Grab the filename stem
    filename_stem = file[:-4].split("\\")[-1]

    # Open raw data and load dataframe
    with open(os.path.join(indir, file)) as infile:

        # Hack here to use a separator that we aren't using so each line gets read in one at a time.
        raw_df = pd.read_csv(infile, sep="\t", header=None, names=["lines"])

    # Transform raw data to a formatted df and a trajectory only dataset
    df, movement_df = pandas_to_csv(raw_df)

    if csv:
        # Save the main dataframe and trajectory data
        save_file(df, filename_stem + ".csv", outdir_for_summary_dfs)
    if movement:
        save_file(movement_df, filename_stem + "_movement.csv", outdir_movement)

    if pdf:
        with PdfPages(os.path.join(outdir_for_pdfs, filename_stem + ".pdf")) as pdf:
            for trial in movement_df["TrialID"].unique():
                print(f"Trial {trial} for {file}")
                graph_trial(movement_df, trial, pdf)


raw_files_csv = []
raw_files_movement = []
raw_files_pdf = []

# If we aren't re-running all subjects, we want to know which ones we've already done.
if rerun_all:

    warnings.warn(
        f"All files in {outdir_base} will be overwritten! \nConsider changing the output base directory instead."
    )
    test = input("Type OVERWRITE DATA to continue: ")
    if test == "OVERWRITE DATA":
        raw_files = raw_files_all
    else:
        exit()

else:
    raw_files_csv = select_files(raw_files_all, outdir_for_summary_dfs)
    raw_files_pdf = select_files(raw_files_all, outdir_for_pdfs)
    raw_files_movement = select_files(raw_files_all, outdir_movement, movement=True)
    raw_files = sorted(
        list(set(raw_files_csv) | set(raw_files_pdf) | set(raw_files_movement))
    )

# Loop through all the raw files and make the summary_dfs and the movement_dfs
for file in raw_files:
    csv = True if file in raw_files_csv else False
    movement = True if file in raw_files_movement else False
    pdf = True if file in raw_files_pdf else False

    run_all(file, csv, movement, pdf)
