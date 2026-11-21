from pathlib import Path
import pandas as pd

from src.expectation_registry import (
    EXPECTED_COLUMNS,
    EXPECTATION_REGISTRY
)

from src.validation import validate_dataframe


def validate_dataset(
    file_path: Path,
    df: pd.DataFrame,
    context,
    data_source
) -> bool:

    file_name = file_path.name

    # Find the corresponding expectation suite
    suite_function = EXPECTATION_REGISTRY.get(file_name)

    if suite_function is None:
        raise ValueError(
            f"No expectation suite registered for: {file_name}"
        )

    # Validate schema first
    schema_success = validate_schema(file_path, df)

    if not schema_success:
        return False

    # Create expectation suite
    suite = suite_function()

    # Execute GX validation
    return validate_dataframe(
        context=context,
        data_source=data_source,
        df=df,
        asset_name=file_path.stem,
        suite=suite
    )


def validate_schema(file_path: Path, df: pd.DataFrame) -> bool:

    expected_columns = EXPECTED_COLUMNS.get(file_path.name)

    if expected_columns is None:
        raise ValueError(
            f"No schema registered for: {file_path.name}"
        )

    actual_columns = df.columns.tolist()

    missing_columns = [
        column for column in expected_columns
        if column not in actual_columns
    ]

    unexpected_columns = [
        column for column in actual_columns
        if column not in expected_columns
    ]

    if missing_columns or unexpected_columns:

        print(f"\nSchema validation failed: {file_path.name}")

        if missing_columns:
            print("Missing columns:", missing_columns)

        if unexpected_columns:
            print("Unexpected columns:", unexpected_columns)

        return False

    print(f"Schema validation passed: {file_path.name}")

    return True