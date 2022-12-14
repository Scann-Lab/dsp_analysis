%{ 
To run this file, uncomment and run the following lines in Matlab: 

trajDir = '.\tests\test_data\Script_Output_DO_NOT_TOUCH\trajectories';
fnOut = '.\tests\test_data\Script_Output_DO_NOT_TOUCH\trajectories\frechet_by_trial.csv';
templateDir = '.\dsp_analysis\dsp_trajectory\templates';
scriptDir = ".\dsp_analysis\dsp_trajectory"
addpath(scriptDir);
trajectory_wrapper(trajDir, fnOut, templateDir)

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
