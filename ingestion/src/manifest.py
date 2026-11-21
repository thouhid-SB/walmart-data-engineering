import json
from pathlib import Path
from datetime import datetime, timezone

MANIFEST_PATH = Path("manifests/ingestion_manifest.json")


def load_manifest() -> list:

    if not MANIFEST_PATH.exists():
        return []

    with MANIFEST_PATH.open("r") as file:
        records = json.load(file)

    return records


def save_manifest(records: list) -> None:

    MANIFEST_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with MANIFEST_PATH.open("w") as file:
        json.dump(records, file, indent=4)


def add_batch_record(batch_record: dict) -> None:

    records = load_manifest()

    records.append(batch_record)

    save_manifest(records)


def update_batch_status(batch_id: str, status: str) -> None:

    records = load_manifest()

    for record in records:

        if record["batch_id"] == batch_id:

            record["status"] = status
            record["updated_at"] = datetime.now(
                timezone.utc
            ).isoformat()

            save_manifest(records)
            return

    raise ValueError(f"Batch not found: {batch_id}")


def find_rejected_batch(file_name: str):

    records = load_manifest()

    for record in reversed(records):

        if (
            record["file_name"] == file_name
            and record["status"] == "REJECTED"
        ):
            return record

    return None


def is_file_already_processed(file_hash: str) -> bool:

    records = load_manifest()

    for record in records:
        if (
            record["file_hash"] == file_hash
            and record["status"] == "UPLOADED"
        ):
            return True

    return False


def find_validated_batch(file_hash: str):

    records = load_manifest()

    for record in reversed(records):
        if (
            record["file_hash"] == file_hash
            and record["status"] == "VALIDATED"
        ):
            return record

    return None