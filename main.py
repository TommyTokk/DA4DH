#!/usr/bin/env python

from src.utils import file_utils as fut
from src.utils import utils as ut
from src.utils import data_understanding as du
from src.utils import plot_utils as plt_ut
import sys
import pandas as pd
import numpy as np


def main():
    args = ut.parse_args()
    try:
        if args.command == "prepare":
            # file_path = args.file
            dir_path = args.directory

            dfs = fut.load_files_from_dir(dir_path)

            # du.get_ICD_groups(dfs[0][0])
            grouped_ICD = du.get_ICD_groups(dfs[0][0])

            # plt_ut.plot_grouped_barplot(grouped_ICD, categories_col='icd_code', group_col='gender', xlabel='ICD Code', ylabel='N. of patients', title="Test")
            # plt_ut.plot_histogram(dfs[0][0]['age'])
            # data=dfs[0][0]['age'].dropna()
            # plt_ut.plot_boxplot(data)
            # plt_ut.plot_histogram(dfs[1][0]['examination_group'])
            #
            outliers = ut.get_IQR_outliers(dfs[1][0]["valuenum"])
            print(type(outliers[0]))
            plt_ut.plot_scatter(
                dfs[1][0]["hadm_id"], dfs[1][0]["valuenum"], outliers=outliers
            )

            # JOIN
            # ...

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
