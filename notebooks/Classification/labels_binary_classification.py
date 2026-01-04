import pandas as pd
import numpy as np
from pathlib import Path


ICDS = {
    "I20", "I21", "I22", "I24", "I25",
    "I30", "I31", "I33",
    "I34", "I35", "I36",
    "I40", "I42",
    "I44", "I45", "I46", "I47", "I48", "I49",
    "I50"
}

ISCHEMIC_CODES = {"I20", "I21", "I22", "I24", "I25"}


def compute_ischemic_label(code_set: set) -> int:
    """
    Assign the ischemic label to a subject based on the set of ICD codes.
    A subject is labeled as ischemic (1) if at least one ICD code
    belongs to the ischemic group (I20–I25). Otherwise, the subject
    is labeled as non-ischemic (0).
    """
    # Compute the intersection between the subject's ICD codes and the predefined ischemic codes
    return int(len(code_set & ISCHEMIC_CODES) > 0)


def generate_ischemic_labels(
    diagnoses_path: str | Path,
    output_path: str | Path | None = None
) -> pd.DataFrame:
    """
    Generate ischemic / non-ischemic labels from heart_diagnoses_1.csv
    """

    diag = pd.read_csv(diagnoses_path)

    # Cleaning
    diag["subject_id"] = diag["subject_id"].astype(str).str.strip()
    # Clean ICD codes:
    # - convert to string
    # - remove leading/trailing spaces
    # - convert to uppercase for consistency
    # - replace empty or invalid string values with NaN
    diag["icd_code"] = (
        diag["icd_code"]
        .astype(str)
        .str.strip()
        .str.upper()
        .replace({"": np.nan, "NAN": np.nan})
    )

    diag = diag[diag["icd_code"].isin(ICDS)].copy()
    if diag.empty:
        raise ValueError("Problems with the format of the ICD codes")

    # For each subject, collect the set of distinct ICD codes
    subject_codes = (
        diag.groupby("subject_id")["icd_code"]
        .unique()
        .reset_index(name="icd_codes")
    )

    # Compute the ischemic label for each subject by applying the rule: at least one ischemic ICD code → label 1
    subject_codes["label_ischemic"] = subject_codes["icd_codes"].apply(
        lambda codes: compute_ischemic_label(set(codes))
    )


    labels_df = subject_codes[["subject_id", "label_ischemic"]]

    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        labels_df.to_csv(output_path, index=False)

    return labels_df
