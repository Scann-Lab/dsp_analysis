import pytest
import os
import pandas as pd
import numpy as np
import glob


def test_sample_data():
    # Expects that the data is somewhere relative to the Analysis script
    scriptDir = os.path.dirname(os.path.realpath(__file__))

    # For testing
    valid_data_path = glob.glob(
        os.path.join(
            scriptDir, "..", "tests", "validation_output", "summary_dfs", "*.csv"
        )
    )
    test_data_path = glob.glob(
        os.path.join(
            scriptDir,
            "..",
            "tests",
            "Script_Output_DO_NOT_TOUCH",
            "summary_dfs",
            "*.csv",
        )
    )

    assert len(valid_data_path) == 1
    assert len(test_data_path) == 1

    valid_df = pd.read_csv(valid_data_path[0])
    test_df = pd.read_csv(test_data_path[0])

    assert valid_df.equals(test_df)
