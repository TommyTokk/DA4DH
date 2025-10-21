import pandas as pd
import os


def load_single_csv(file_path):
    return pd.read_csv(file_path)


def load_files_from_dir(dir_path: str) -> list:

    res = []

    if not os.path.isdir(dir_path):
        exit("Path is not a dir")

    for file in sorted(os.listdir(dir_path)):
        res.append((pd.read_csv(f"{dir_path}/{file}"), file))

    return res
