# Analysis code for the Unity version of the Dual Solution Paradigm

1. Install Anaconda and VSCode 
2. Git clone the dsp_analysis repo onto your local machine. 
3. Create the conda environment with an Anaconda Prompt `conda env -n dsp-analysis create environment.yml`
4. Place all the raw DSP output files in the same directory
5. File -> Open Folder -> open the local git repo you cloned (dsp_analysis). 
6. In the terminal, paste the following command after changing your input directory to the folder where your raw files are. You can select any output directory you like. 
`conda run -n dsp-analysis python .dspy\run_dspy.py -i "[full path to directory containing raw files]" -o "[full path to output directory of your choice]"`
7. Next, open Matlab and run `trajectory_wrapper.m`. Be sure to change the scriptDir and the trajDir as instructed in that file. 
8. Save a copy of the meta data matching the columns of `.\tests\test_data\meta_data.csv` 
9. Finally, back in the terminal, paste the following command
`conda run -n dsp-analysis python .\dspy\merge_dspy.py -i "[full path to the directory containing the OUTPUT of the previous steps"] -m "[full path to your metadata file]" - o "[full path to desired output file]`
