import pandas as pd
from pathlib import Path


def read_csv(file_path: Path) -> pd.DataFrame:

    df = pd.read_csv(file_path)

    return df