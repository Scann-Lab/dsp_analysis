# To run in VS code with dsp-analysis conda env: conda run -n dsp-analysis pytest .\tests\test_1_sample_data.py -W ignore::DeprecationWarning:

import os
import sys
import pytest

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "dspy"))
import pandas as pd
import numpy as np
import glob
import process_dsp_data
import shutil

def test_sample_data():

    # Expects that the data is somewhere relative to the Analysis script
    scriptDir = os.path.dirname(os.path.realpath(__file__))
    # We compare two directories: validation directory and the new output of this test.
    test_data_path = os.path.join(scriptDir, "test_data", "test_output")

    valid_data_path = os.path.join(scriptDir, "test_data", "validation_output")

    # If files already exist, we want to remove them.
    test_data_files = glob.glob(
        os.path.join(
            test_data_path,
            "summary_dfs",
            "*.csv",
        )
    )

    if len(test_data_files) >= 1:
        shutil.rmtree(test_data_path)

    # Generate the new output from the test.
    process_dsp_data.process_dsp_data(
        os.path.join(scriptDir, "test_data"),
        test_data_path,
        rerun=False,
        scriptDir=scriptDir,
        all_pdfs=False,
    )

    # For testing
    valid_summary_files = sorted(
        glob.glob(
            os.path.join(
                valid_data_path,
                "summary_dfs",
                "*.csv",
            )
        )
    )

    test_summary_files = sorted(
        glob.glob(
            os.path.join(
                test_data_path,
                "summary_dfs",
                "*.csv",
            )
        )
    )
    
    # Compare the summary dfs
    for i, j in enumerate(valid_summary_files):

        assert (
            valid_summary_files[i].split(os.sep)[-1]
            == test_summary_files[i].split(os.sep)[-1]
        )

        valid_summary_df = pd.read_csv(valid_summary_files[i])
        test_summary_df = pd.read_csv(test_summary_files[i])

        assert valid_summary_df.equals(test_summary_df)

    valid_movement_files = sorted(
        glob.glob(os.path.join(valid_data_path, "raw_movement_data", "*.csv"))
    )
    test_movement_files = sorted(
        glob.glob(os.path.join(test_data_path, "raw_movement_data", "*.csv"))
    )

    for i, j in enumerate(valid_movement_files):

        assert (
            valid_summary_files[i].split(os.sep)[-1]
            == test_summary_files[i].split(os.sep)[-1]
        )

        valid_movement_df = pd.read_csv(valid_movement_files[i])
        test_movement_df = pd.read_csv(test_movement_files[i])

        assert valid_movement_df.equals(test_movement_df)

    assert len(valid_movement_files) > 0
    assert len(valid_summary_files) > 0
