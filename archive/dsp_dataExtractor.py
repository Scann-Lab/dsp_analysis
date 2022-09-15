## Written by Alex Boone
## Modified by Steven Weisberg
## Last edit: 7/21/2022

### Purpose of this script is to process location data from the Dual Solution
### Paradigm, built in Unity 3D. It will output a set of images that can be
### hand-coded to determine A) Success, and B) which path was taken (familiar
### route or novel shortcut).

from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages
from imageio import imread
import os
from shutil import copyfile
import glob

# Do you want to see previews of the figures
show_plots = False

# Do you want to re-run all subjects?
rerun_all = False


# ******************************************************************************************************
#                                         Finding the Files
# ******************************************************************************************************

# Expects that the data is somewhere relative to the Analysis script
scriptDir = os.path.dirname(os.path.realpath(__file__))


# Where are the raw data?
indir = os.path.join(scriptDir, "..", "DSP_RawData")

# These should be set relative to the code directory.
outdir_backup = os.path.join(
    scriptDir, "..", "DSP_RawData", "Script_Output_DO_NOT_TOUCH_new_version"
)

os.makedirs(outdir_backup, exist_ok=True)

# Select all text files corresponding to test (e.g., NOT listed with Training or Ranking in the filename)
raw_files_all = list(
    set(glob.glob(indir + "//*.txt"))
    - set(glob.glob(indir + "//*Training*"))
    - set(glob.glob(indir + "//*Ranking*"))
)


# If we aren't re-running all subjects, we want to know which ones we've already done.
if rerun_all:
    raw_files = raw_files_all
else:
    exclude_files = []
    already_coded_stems = []
    already_coded = os.listdir(outdir_backup)
    for i in already_coded:
        if "Participant" in i and ".pdf" in i:
            already_coded_stems.append(i[:-4] + ".txt")
    for i in already_coded_stems:
        exclude_files += [f for f in raw_files_all if i in f]

    raw_files = list(set(raw_files_all) - set(exclude_files))


# ******************************************************************************************************
#                                         PLOTTER
# ******************************************************************************************************


def Graph(trialID, expPrefix):
    pyplot.figure(dpi=350)
    figureFiletype = ".png"
    pyplot.plot(PosX_array, PosY_array, "k", label="__nolegend__")

    v = [0, 222, 0, 222]
    pyplot.axis(v)
    pyplot.ylabel("Y")
    pyplot.xlabel("X")
    pyplot.title(title)
    pyplot.legend(["Path"], loc="center left", bbox_to_anchor=(1.0, 0.5))

    # Open the image with that trial structure
    imageFilename = expPrefix + trialID + figureFiletype
    bestImage = os.path.join(scriptDir, "Nav_stratAbility_Maps", imageFilename)
    img = imread(bestImage)

    pyplot.imshow(
        img, zorder=0, extent=[0.0, 222.0, 0.0, 222.0]
    )  # left right bottom top

    pp.savefig()
    pyplot.clf()


# define Python user-defined exceptions
class NoAltExpError(Exception):
    """Raised when alt experiment not recognized"""

    pass


if not show_plots:
    pyplot.ioff()

currTrial = ""
Alt_Exp = ""
TrialID = ""
title = ""
expPrefix = ""

for f in raw_files:
    # the first file in each directory was this for some reason
    if "txt" in f:
        print(f)
        numOfLines = 0
        Trial_Count = 0

        with open(os.path.join(indir, f)) as infile:
            filename = f[:-4].split("\\")[-1] + ".pdf"
            try:
                pp = PdfPages(os.path.join(outdir_backup, filename))
            except PermissionError:
                print("Could not open PDF - delete or alter permissions and try again.")
                continue

            PosX_array = []
            PosY_array = []
            headerLines = 0
            prev_line = ""

            for current_line in infile:

                if (current_line.startswith("!!")) and not "Encoding" in prev_line:
                    if Trial_Count > 0:
                        Graph(currTrial, expPrefix)
                        PosX_array = []
                        PosY_array = []

                    Trial_Count += 1

                    title = current_line[2:]
                    title_split = current_line.split("_")
                    trialID = title_split[2]
                    trialID = trialID[0:2]
                    currTrial = trialID

                    print(title)

                elif "DSPType" in current_line:
                    Alt_Exp = current_line.strip()

                    while True:
                        try:

                            if Alt_Exp == "DSPType: 2":
                                expPrefix = "DSP2_"
                            elif Alt_Exp == "DSPType: 1":
                                expPrefix = "DSP1_"
                            else:
                                raise NoAltExpError
                            break
                        except NoAltExpError:
                            print(
                                "Environment type not found. Make sure DSPType is set to 1 or 2.\n"
                            )

                # Gets x,z coordinates from each line and puts into array
                elif Trial_Count > 0:
                    no_time_line = current_line.split("  ")
                    movement = no_time_line[1].split(",")
                    x = float(movement[0])
                    y = float(movement[1])

                    PosX_array.append(x)
                    PosY_array.append(y)

                # Plots the last trial

                prev_line = current_line

            else:
                Graph(currTrial, expPrefix)
                PosX_array = []
                PosY_array = []

            pp.close()

            pyplot.close()
