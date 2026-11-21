import hashlib
from pathlib import Path
from datetime import datetime, timezone


def calculate_file_hash(file_path: Path) -> str:

    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:

        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def get_file_metadata(file_path: Path) -> dict:

    file_stats = file_path.stat()

    metadata = {
        "file_name": file_path.name,
        "file_size": file_stats.st_size,
        "last_modified": datetime.fromtimestamp(
            file_stats.st_mtime,
            tz=timezone.utc
        ).isoformat(),
        "file_hash": calculate_file_hash(file_path)
    }

    return metadata