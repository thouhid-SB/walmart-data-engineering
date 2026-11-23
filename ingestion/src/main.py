
from src.discovery import discover_csv_files
from src.config_loader import load_config
from src.file_tracker import get_file_metadata
from src.reader import read_csv
from src.rejected_handler import move_to_rejected

from src.validation import (
    get_gx_context,
    register_data_source
)

from src.dataset_validator import validate_dataset
from src.batch_manager import get_or_create_batch

from src.manifest import update_batch_status

from src.s3_uploader import upload_csv_to_s3


def main():

    config = load_config()

    source_dir = config["source"]["directory"]
    bucket_name = config["aws"]["bucket_name"]
    load_type = config["s3"]["load_type"]
    raw_prefix = config["s3"]["raw_prefix"]

    csv_files = discover_csv_files(
        source_dir,
        config["source"]["file_pattern"]
    )

    if not csv_files:
        print("No CSV files found.")
        return

    context = get_gx_context()
    data_source = register_data_source(context)

    for file in csv_files:

        metadata = get_file_metadata(file)
        metadata["load_type"] = load_type

        batch_record = get_or_create_batch(metadata)

        if batch_record is None:
            continue

        batch_id = batch_record["batch_id"]
        batch_load_type = batch_record["load_type"]

        print(f"\nFile: {metadata['file_name']}")
        print(f"Batch ID: {batch_id}")
        print(f"Load type: {batch_load_type}")

        # Validation
        if batch_record["status"] not in ("VALIDATED", "UPLOADED"):

            df = read_csv(file)

            print(f"Rows: {len(df)}")
            print(f"Columns: {df.columns.tolist()}")

            validation_success = validate_dataset(
                file_path=file,
                df=df,
                context=context,
                data_source=data_source
            )

            if not validation_success:

                print(f"Validation failed: {file.name}")

                try:
                    move_to_rejected(file)
                except FileExistsError as error:
                    print(f"Could not move rejected file: {error}")
                    continue

                update_batch_status(batch_id, "REJECTED")
                continue

            update_batch_status(batch_id, "VALIDATED")
            print(f"Validation passed: {file.name}")

        else:
            print("Validation already completed.")

        # S3 upload
        try:
            upload_csv_to_s3(
                file_path=file,
                bucket_name=bucket_name,
                batch_id=batch_id,
                load_type=batch_load_type,
                raw_prefix=raw_prefix
            )

            update_batch_status(batch_id, "UPLOADED")
            print(f"Batch completed successfully: {batch_id}")

        except Exception as error:
            print(f"S3 upload failed: {error}")
            raise


if __name__ == "__main__":
    main()
