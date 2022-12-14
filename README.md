# Analysis code for the Unity version of the Dual Solution Paradigm

1. Install Anaconda and VSCode 
2. Git clone the dsp_analysis repo onto your local machine. 
3. Create the conda environment with an Anaconda Prompt `conda env -n dsp-analysis create environment.yml`
4. Place all the raw DSP output files in the same directory
5. File -> Open Folder -> open the local git repo you cloned (dsp_analysis). 
6. In the terminal, paste the following command after changing your input directory to the folder where your raw files are. You can select any output directory you like. 
`conda run -n dsp-analysis python .\run_dspy.py -i "[full path to directory containing raw files]" -o "[full path to output directory of your choice]"`