# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 16:12:30 2022

@author: stevenweisberg
"""
import os
import glob
import pandas as pd
import xlrd
import numpy as np

scriptDir = os.getcwd()

# Expects that the data is one file up from the analysis script
os.chdir(os.path.dirname(os.getcwd()))
masterDir = os.getcwd()


outdir_backup = os.path.join(masterDir,'DSP_RawData','Script_Output_DO_NOT_TOUCH')

files = glob.glob(outdir_backup + os.sep + '*.xlsx')

tallies = pd.DataFrame(columns={'participant','success_40','success_60'})

for file in files:
    df = pd.read_excel(file)
    
    success_40 = df.groupby('Status')['ParticipantNo'].count()['Success']

    
    conds = [
        (df['Status'] == 'Success') & (df['Time Elapsed'] > 39.9),
        (df['Status'] == 'Success') & (df['Time Elapsed'] < 39.9),
        (df['Status'] == 'Failure')
        ]
    
    values = ['Failure','Success','Failure']
    
    
    df['Status_60'] = np.select(conds,values)
    
    try:
        success_60 = df.groupby('Status_60')['ParticipantNo'].count()['Success']
    except:
        success_60 = 0
        
    p_tallies = {'participant':df['ParticipantNo'][0],
                 'success_40':success_40,
                 'success_60':success_60}
    
    tallies = tallies.append(p_tallies,ignore_index=True)
    
print('h')