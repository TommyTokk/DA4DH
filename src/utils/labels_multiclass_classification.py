import pandas as pd
import numpy as np
from pathlib import Path


ICDS = {
    "I20", "I21", "I22", "I24", "I25",          # Ischemic
    "I44", "I45", "I46", "I47", "I48", "I49",   # Arrhythmias / conduction / cardiac arrest
    "I34", "I35", "I36", "I50", "I42",          # Valvular & pump failure
    "I30", "I31", "I33", "I40"                  # Inflammatory / structural
}


MULTICLASS_MAPPING = {
    0: {"I20", "I21", "I22", "I24", "I25"},                # Ischemic heart disease
    1: {"I44", "I45", "I46", "I47", "I48", "I49"},         # Arrhythmias / conduction / cardiac arrest
    2: {"I34", "I35", "I36", "I50", "I42"},                # Valvular & pump failure
    3: {"I30", "I31", "I33", "I40"},                       # Inflammatory / structural
}

CLASS_NAMES = {
    0: "Ischemic heart disease",
    1: "Arrhythmias, conduction disorders and cardiac arrest",
    2: "Valvular and pump failure disorders",
    3: "Inflammatory and structural heart disease",
}


def compute_multiclass_label(code_set: set) -> int:
    """
    Assign a multiclass label to a subject based on ICD codes.
    Priority ruleIf multiple classes are present, the most clinically severe category is selected following the order:
      Ischemic > Arrhythmias > Valvular/Pump failure > Inflammatory
    """

    # Iterate over class identifiers in increasing order.
    for class_id in sorted(MULTICLASS_MAPPING.keys()):
        # Check whether at least one ICD code of the subject belongs to the current class
        if len(code_set & MULTICLASS_MAPPING[class_id]) > 0:
            return class_id

    raise ValueError("No valid ICD code found for subject")


def generate_multiclass_labels(
    diagnoses_path: str | Path,
    output_path: str | Path | None = None
) -> pd.DataFrame:
    """
    Generate multiclass cardiovascular labels from heart_diagnoses_1.csv using clinically meaningful ICD groupings.
    The implementation mirrors the binary labeling pipeline provided.
    """
    # Load the diagnoses dataset
    diag = pd.read_csv(diagnoses_path)

    # Cleaning
    diag["subject_id"] = diag["subject_id"].astype(str).str.strip()
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

    # Assign a single multiclass label to each subject using the predefined clinical priority rule
    subject_codes["label_multiclass"] = subject_codes["icd_codes"].apply(
        lambda codes: compute_multiclass_label(set(codes))
    )

    labels_df = subject_codes[["subject_id", "label_multiclass"]]

    # Optional saving
    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        labels_df.to_csv(output_path, index=False)

    return labels_df
