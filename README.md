# Analysis code for the Unity version of the Dual Solution Paradigm

[![Python application](https://github.com/Scann-Lab/dsp_analysis/actions/workflows/python-app.yml/badge.svg)](https://github.com/Scann-Lab/dsp_analysis/actions/workflows/python-app.yml)

## Installation (for Windows only)
1. Install Anaconda and VSCode 
2. Git clone the dsp_analysis repo onto your local machine. 
3. Open an Anaconda Prompt and change directory to the parent directory of the Github repository. 
4. Create the conda environment with an Anaconda Prompt `conda env create -n dsp-analysis environment.yml`
5. To test your installation, open VSCode and go to File -> Open Folder -> open the local git repo you cloned (dsp_analysis). 
6. Test that the software is running properly. To do so, execute the following command in the terminal. `conda run -n dsp-analysis pytest .\tests\test_1_sample_data.py -W ignore::DeprecationWarning:`
7. Verify that all tests were passed. 

## Running the scripts
1 Place all the raw DSP output files in the same directory
2. In VS Coe, in a terminal, paste the following command. Be sure to change the input directory to the folder where your raw files are. You can select any output directory you like. 
`conda run -n dsp-analysis python .dspy\run_dspy.py -i "[full path to directory containing raw files]" -o "[full path to output directory of your choice]"`
3. Next, open Matlab and run `trajectory_wrapper.m`. Be sure to change the scriptDir and the trajDir as instructed in that file. 
4. Save a copy of the meta data matching the columns of `.\tests\test_data\meta_data.csv` 
5. Finally, back in the terminal, paste the following command
`conda run -n dsp-analysis python .\dspy\merge_dspy.py -i "[full path to the directory containing the OUTPUT of the previous steps"] -m "[full path to your metadata file]" - o "[full path to desired output file]`
