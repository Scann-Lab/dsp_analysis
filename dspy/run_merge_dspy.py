import sys
import os

scriptDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(scriptDir, "..", "dspy"))
import merge_dspy

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Merge DSP data")
    parser.add_argument("-i", "--indir", help="Data directory for input", required=True)
    parser.add_argument(
        "-o", "--outdir", help="Output directory to save results", required=True
    )
    parser.add_argument("-m", "--meta", help="Meta data file", required=True)

    args = vars(parser.parse_args())

    merge_dspy.merge_dspy(args["indir"], args["meta"], args["outdir"])
