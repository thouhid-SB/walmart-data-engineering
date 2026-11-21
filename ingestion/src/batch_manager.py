from uuid import uuid4
from datetime import datetime, timezone

from src.manifest import (
    add_batch_record,
    find_rejected_batch,
    find_validated_batch,
    is_file_already_processed,
    load_manifest,
    save_manifest
)


def generate_batch_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%d_%H%M%S"
    )
    unique_id = uuid4().hex[:8]

    return f"BATCH_{timestamp}_{unique_id}"


def get_or_create_batch(metadata: dict):

    file_name = metadata["file_name"]
    file_hash = metadata["file_hash"]
    load_type = metadata["load_type"]

    # Skip previously uploaded files
    if is_file_already_processed(file_hash):
        print(f"Already processed: {file_name}")
        return None

    # Recover a rejected batch
    rejected_batch = find_rejected_batch(file_name)

    if rejected_batch:
        records = load_manifest()

        for record in records:
            if record["batch_id"] == rejected_batch["batch_id"]:
                record["file_hash"] = file_hash
                record["file_size"] = metadata["file_size"]
                record.setdefault("load_type", load_type)
                record["status"] = "VALIDATING"
                record["attempt"] += 1
                record["updated_at"] = datetime.now(
                    timezone.utc
                ).isoformat()

                rejected_batch = record
                break

        save_manifest(records)

        print(f"Retrying batch: {rejected_batch['batch_id']}")
        return rejected_batch

    # Recover a previously validated batch
    validated_batch = find_validated_batch(file_hash)

    if validated_batch:
        records = load_manifest()

        for record in records:
            if record["batch_id"] == validated_batch["batch_id"]:
                # Add load_type to older manifest records
                if "load_type" not in record:
                    record["load_type"] = load_type

                validated_batch = record
                break

        save_manifest(records)

        print(
            f"Resuming upload for batch: "
            f"{validated_batch['batch_id']}"
        )
        return validated_batch

    # Create a new batch
    batch_record = {
        "batch_id": generate_batch_id(),
        "file_name": file_name,
        "file_hash": file_hash,
        "file_size": metadata["file_size"],
        "load_type": load_type,
        "status": "VALIDATING",
        "attempt": 1,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    add_batch_record(batch_record)

    return batch_record