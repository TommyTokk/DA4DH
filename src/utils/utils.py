import argparse


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
