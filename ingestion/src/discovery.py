from pathlib import Path


def discover_csv_files(directory: str, pattern: str) -> list[Path]:

    data_dir = Path(directory)

    if not data_dir.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    csv_files = sorted(data_dir.glob(pattern))

    return csv_files