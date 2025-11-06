import argparse
import os
import pandas as pd
import functools as ft
import numpy as np
from scipy.stats import iqr
from src.utils import data_understanding as du


def parse_args():
    """
    Parse command line arguments using a subcommand structure.

    Returns:
        argparse.Namespace: Object containing all parsed arguments
    """

    # Create main parser
    parser = argparse.ArgumentParser(
        description="CSV analysis and manipulation tool for DA",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    subparsers.required = True

    # === DATA PREPARATION ===
    data_preparation_parser = subparsers.add_parser(
        "prepare", help="Prepare data to be analysed"
    )
    data_preparation_parser.add_argument(
        "-f", "--file", help="Path to the csv file to load"
    )

    data_preparation_parser.add_argument(
        "-d",
        "--directory",
        help="Path to the directory containing the csv files to load",
    )

    data_preparation_parser.add_argument(
        "-n",
        "--num-files",
        help="Number of files to load from the specified directory. If none all the files will be loaded",
    )

    # === DATA PROCESSING ===

    data_processing_parser = subparsers.add_parser("process", help="Process the data ")

    return parser.parse_args()


def create_report(df: pd.DataFrame, file_name: str, output_path="outputs/reports"):
    # create the dir if not exists
    os.makedirs(output_path, exist_ok=True)

    # create the output file
    output_file = os.path.join(output_path, f"{file_name}.txt")

    """
        ==== Data understanding on file ====
        ====================================

        Shape:
            rows:...
            cols:...
        
        Num. dups: ...

        .
        .
        .
        
    """

    with open(output_file, "w") as of:
        of.write(f"==== Data understanding on {file_name} ====\n")
        of.write("=" * 50)
        of.write("\n\n")

        n_rows = df.shape[0]
        n_cols = df.shape[1]

        of.write("Shape:\n")
        of.write(f"  Rows: {n_rows}\n")
        of.write(f"  Cols: {n_cols}\n\n")

        of.write(f"Number of duplicates: {du.get_num_dups(df)}")


# === IQR ===
#
def get_IQR_outliers(values):
    data_iqr = iqr(values.dropna())

    outliers = []

    lower_bound = np.quantile(values.dropna(), 0.25) - (1.5 * data_iqr)
    upper_bound = np.quantile(values.dropna(), 0.75) + (1.5 * data_iqr)

    for el in values:
        if el < lower_bound or el > upper_bound:
            outliers.append(el)

    return outliers
