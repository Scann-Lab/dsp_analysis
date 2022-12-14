import os
from shutil import copyfile
import glob
import pandas as pd
import numpy as np
from imageio import imread


# Expects that the data is somewhere relative to the Analysis script
scriptDir = os.path.dirname(os.path.realpath(__file__))


# Where are the raw data?
indir = os.path.join(
    scriptDir, "..", "DSP_RawData", "Script_Output_DO_NOT_TOUCH_new_version"
)

raw_files_all = list(
    set(glob.glob(indir + "//*.csv")) - set(glob.glob(indir + "//*movement*"))
)

df = pd.read_csv(raw_files_all[0])

for file in raw_files_all:

    df = df.append(pd.read_csv(file))


df["Outcome"] = np.where(df["Status"].str.contains("Success"), 1, 0)

df["aging"] = np.where(df["ParticipantNo"].astype(str).str[0] == "1", "young", "old")
df["sex"] = np.where(df["ParticipantNo"].astype(str).str[1] == "1", "male", "female")

df.head()

import seaborn as sns
import matplotlib.pyplot as plt

part_level = df.groupby(["ParticipantNo"], as_index=False).agg(
    {
        "Time Elapsed": "mean",
        "Distance": "mean",
        "Time_to_First_Movement": "mean",
        "Outcome": "mean",
        "sex": "first",
        "aging": "first",
        "DSPType": "first",
        "FailTime": "first",
    }
)

sns.swarmplot(data=part_level, x="aging", hue="sex", y="Outcome")
plt.show()
sns.swarmplot(data=part_level, x="aging", hue="sex", y="Distance")
plt.show()
sns.swarmplot(data=part_level, x="aging", hue="sex", y="Time_to_First_Movement")
plt.show()
sns.swarmplot(data=part_level, x="aging", hue="sex", y="Time Elapsed")
plt.show()


# %%
import scipy.stats as stats


print(
    stats.ttest_ind(
        part_level[part_level["aging"] == "young"]["Outcome"],
        part_level[part_level["aging"] == "old"]["Outcome"],
    )
)


print(
    stats.ttest_ind(
        part_level[part_level["aging"] == "young"]["Distance"],
        part_level[part_level["aging"] == "old"]["Distance"],
    )
)

print(
    stats.ttest_ind(
        part_level[part_level["aging"] == "young"]["Time_to_First_Movement"],
        part_level[part_level["aging"] == "old"]["Time_to_First_Movement"],
    )
)

