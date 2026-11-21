
from pathlib import Path

from src.reader import read_csv
from src.validation import (
    get_gx_context,
    register_data_source
)
from src.dataset_validator import validate_dataset


DATA_DIR = Path("data/incoming")


def test_all_datasets():

    context = get_gx_context()
    data_source = register_data_source(context)

    results = {}

    for file_path in sorted(DATA_DIR.glob("*.csv")):

        print(f"\n{'=' * 50}")
        print(f"DATASET: {file_path.name}")
        print("=" * 50)

        # Read CSV once
        df = read_csv(file_path)

        # Validate using the existing DataFrame
        success = validate_dataset(
            file_path=file_path,
            df=df,
            context=context,
            data_source=data_source
        )

        results[file_path.name] = success

    print("\nFINAL VALIDATION SUMMARY")
    print("=" * 50)

    for file_name, success in results.items():
        print(
            f"{file_name}: "
            f"{'PASSED' if success else 'FAILED'}"
        )

    assert len(results) == 6, (
        f"Expected 6 datasets, found {len(results)}"
    )

    failed_datasets = [
        name for name, success in results.items()
        if not success
    ]

    assert not failed_datasets, (
        f"Validation failed for: {failed_datasets}"
    )
