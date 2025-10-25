#!/usr/bin/env python

from src.utils import file_utils as fut
from src.utils import utils as ut
from src.utils import data_understanding as du
import sys
import pandas as pd

def main():
    args = ut.parse_args()
    try:
        if args.command == "prepare":
            # file_path = args.file
            dir_path = args.directory

            dfs = fut.load_files_from_dir(dir_path)

            #du.get_ICD_groups(dfs[0][0])

            print(du.get_nums_of_abnormal(dfs[1][0]).head(10))

            #JOIN
            #...

            # GENERATE REPORT FOR JOINED

            # TODO: Data Understanding
            # 1) Percentuale di colonne non None
            # 2) Numero di duplicati
            # 3) Statistiche delle colonne numeriche

    except Exception as e:
        print(f"Error during execution: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
