%{ 
%To run this file, change the scriptDir to the parent directory of the 
%git repository, then copy and run the following lines in Matlab: 

%Change this line to the path for your script directory!
scriptDir = 'C:\Users\stevenweisberg\Documents\dsp_analysis';

%Change this line to the path for your trajectories directory
%(allTrajectories_1.csv and allTrajectories_2.csv)
trajDir = horzcat(scriptDir, '\tests\test_data\validation_output\trajectories');


fnOut = horzcat(trajDir, '\frechet_by_trial.csv');
templateDir = horzcat(scriptDir, '\dsp_trajectory\templates');
addpath(horzcat(scriptDir, '\dsp_trajectory\matlab'));
trajectory_wrapper(trajDir, fnOut, templateDir);

%}


function trajectory_wrapper (trajDir, fnOut, templateDir)

cd(templateDir);

for dspVersion = 1:2
    fnSubjectData = horzcat(trajDir, filesep, 'allTrajectories_', int2str(dspVersion), '.csv');
    fnMapCoords = horzcat(templateDir, filesep, 'dsp_coords_version_',int2str(dspVersion), '.txt');
    fnMapLMs = horzcat(templateDir, filesep, 'lmOnPath_version_',int2str(dspVersion),'.txt');
    createSubjectTrialData (fnSubjectData, fnMapCoords, fnMapLMs, trajDir);
end
[fdTableAll] = createFdTables (trajDir, fnOut, 0, 0);

end
