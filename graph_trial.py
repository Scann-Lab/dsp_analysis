# %%

import matplotlib.pyplot as plt
from imageio import imread
import os
import pandas as pd
import glob


# Expects that the data is somewhere relative to the Analysis script
scriptDir = os.path.dirname(os.path.realpath(__file__))


# Where are the raw data?
indir = os.path.join(scriptDir,'..','DSP_RawData','Script_Output_DO_NOT_TOUCH_new_version')


def graph_trial(df):

    trial_id = df['TrialID'][0]

    try:
        assert df['TrialID'].nunique()==1, f'Trial: {trial_id}'
    except:
        raise ValueError('DataFrame must have only one value for TrialID.')

    

    plt.figure(dpi = 350)
    figureFiletype = ".png"
    plt.plot(df['x'],df['z'], "k", label = "__nolegend__")

    v = [0, 222, 0, 222]
    plt.axis(v)
    plt.ylabel("Y")
    plt.xlabel("X")
    plt.title(trial_id)
    plt.legend(["Path"], loc = 'center left', bbox_to_anchor = (1.0, 0.5))



    # Open the image with that trial structure
    imageFilename = trial_id.upper() + figureFiletype
    bestImage = os.path.join(scriptDir,'Nav_stratAbility_Maps',imageFilename)
    img = imread(bestImage)

    plt.imshow(img,zorder=0,extent=[0.0, 222.0, 0.0, 222.0]) #left right bottom top
    plt.show()

movement_files_all = list(set(glob.glob(indir + '//*Participant_22*movement*')))

movement_df = pd.read_csv(movement_files_all[0])

graph_trial(movement_df[movement_df['TrialID'] ==  movement_df['TrialID'][0]])

# %%
