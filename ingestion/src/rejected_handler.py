import shutil
from pathlib import Path


def move_to_rejected(file_path: Path) -> Path:

    rejected_dir = Path("data/rejected")

    # Create rejected directory if it doesn't exist
    rejected_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    destination = rejected_dir / file_path.name

    # Avoid overwriting an existing rejected file
    if destination.exists():
        raise FileExistsError(
            f"Rejected file already exists: {destination}"
        )

    shutil.move(
        str(file_path),
        str(destination)
    )

    print(f"Moved to rejected: {destination}")

    return destination