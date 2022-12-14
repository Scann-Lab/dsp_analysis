import sys
import os

scriptDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(scriptDir, "..", "dspy"))
import process_dsp_data

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process all DSP data.")
    parser.add_argument("-i", "--indir", help="Data directory for input", required=True)
    parser.add_argument(
        "-o", "--outdir", help="Output directory to save results", required=True
    )
    parser.add_argument(
        "-r", "--rerun", help="Perform validation", required=False, action="store_true"
    )
    parser.add_argument(
        "-s",
        "--scriptdir",
        help="Directory where the scripts are for this",
        required=False,
    )

    parser.set_defaults(scriptdir=scriptDir, val=False)

    args = vars(parser.parse_args())

    process_dsp_data.process_dsp_data(
        args["indir"], args["outdir"], args["rerun"], args["scriptdir"]
    )
