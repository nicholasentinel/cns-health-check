import os
import glob
import pandas as pd

def parse_framework_csv(data_dir="data"):
    """
    Searches for files matching data/exported_framework-*.csv, picks the most
    recently modified one, and returns a dict mapping each unique Framework
    to its average posture score (float).

    Raises:
      FileNotFoundError if no matching CSV exists.
      KeyError if the required columns ("Framework", "posture score") are missing.
    """
    pattern = os.path.join(data_dir, "exported_framework-*.csv")
    matches = glob.glob(pattern)
    if not matches:
        raise FileNotFoundError(f"No files found matching '{pattern}'")

    latest_csv = max(matches, key=os.path.getmtime)
    df = pd.read_csv(latest_csv)

    required_cols = {"Framework", "Posture Score"}
    if not required_cols.issubset(set(df.columns)):
        missing = required_cols - set(df.columns)
        raise KeyError(f"Missing columns in {latest_csv}: {missing}")

    df = df.dropna(subset=["Framework", "Posture Score"])
    df["Posture Score"] = df["Posture Score"].astype(float)
    grouped = df.groupby("Framework", as_index=False)["Posture Score"].mean()

    return dict(zip(grouped["Framework"], grouped["Posture Score"]))
