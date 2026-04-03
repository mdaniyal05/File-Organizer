#!/usr/bin/env python3

import argparse
import shutil
from pathlib import Path
from collections import defaultdict

MISC_FOLDER = "Miscellaneous"

OTHER_FOLDER = "Other"

DRY_RUN = False

EXTENSION_MAP = {
    # Images
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images",
    ".bmp": "Images", ".svg": "Images", ".webp": "Images",

    # Documents
    ".pdf": "Documents", ".doc": "Documents", ".docx": "Documents",
    ".txt": "Documents", ".md": "Documents", ".rtf": "Documents",
    ".xls": "Documents", ".xlsx": "Documents", ".ppt": "Documents",
    ".pptx": "Documents", ".odt": "Documents",

    # Archives
    ".zip": "Archives", ".tar": "Archives", ".gz": "Archives",
    ".bz2": "Archives", ".7z": "Archives", ".rar": "Archives",

    # Code & Scripts
    ".py": "Code", ".js": "Code", ".html": "Code", ".css": "Code",
    ".cpp": "Code", ".c": "Code", ".java": "Code", ".json": "Code",
    ".xml": "Code", ".yaml": "Code", ".yml": "Code",

    # Audio
    ".mp3": "Audio", ".wav": "Audio", ".flac": "Audio", ".aac": "Audio",

    # Video
    ".mp4": "Video", ".mkv": "Video", ".avi": "Video", ".mov": "Video",
}


def get_destination_folder(ext: str) -> str:
    ext = ext.lower()
    return EXTENSION_MAP.get(ext, OTHER_FOLDER)


def safe_move(src: Path, dest_dir: Path) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / src.name

    if dest_path.exists():
        stem = src.stem
        suffix = src.suffix
        counter = 1
        while dest_path.exists():
            new_name = f"{stem}_{counter}{suffix}"
            dest_path = dest_dir / new_name
            counter += 1

    if DRY_RUN:
        print(f"[DRY RUN] Would move '{src}' -> '{dest_path}'")
    else:
        shutil.move(str(src), str(dest_path))
        print(f"Moved '{src}' -> '{dest_path}'")


def organize_directory(directory: Path) -> None:
    if not directory.exists() or not directory.is_dir():
        print(f"Error: '{directory}' is not a valid directory.")
        return

    print(f"Organizing files in: {directory.absolute()}")
    if DRY_RUN:
        print("DRY RUN MODE – no files will actually be moved\n")

    files_by_folder = defaultdict(list)

    for item in directory.iterdir():
        if item.is_dir() or item.name.startswith('.'):
            continue

        if item.suffix == "":
            files_by_folder[MISC_FOLDER].append(item)
        else:
            folder = get_destination_folder(item.suffix)
            files_by_folder[folder].append(item)

    for folder_name, files in files_by_folder.items():
        dest_dir = directory / folder_name
        for file_path in files:
            safe_move(file_path, dest_dir)

    print("\nOrganization complete!")


def main():
    parser = argparse.ArgumentParser(
        description="Organize files in a directory by their extensions."
    )
    parser.add_argument(
        "directory", nargs="?", default=".",
        help="Path to the directory to organize (default: current directory)."
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Simulate the organization without moving any files."
    )
    args = parser.parse_args()

    global DRY_RUN
    if args.dry_run:
        DRY_RUN = True

    target_dir = Path(args.directory).resolve()
    organize_directory(target_dir)


if __name__ == "__main__":
    main()
