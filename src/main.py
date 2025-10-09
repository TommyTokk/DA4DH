#!/usr/bin/env python

from utils import file_utils as fut
from utils import utils as ut
import sys


def main():
    args = ut.parse_args()
    try:
        if args.command == "prepare":
            file_path = args.file
            df = fut.load_single_csv(file_path)
            print(df.describe())
            print(df.info())
    except Exception as e:
        print(f"Error during execution: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
