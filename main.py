#!/usr/bin/env python3
"""A 32-character Wi-Fi name that is a tiny story.

The program drops one network name into /output/entry.txt. The first
half sounds reassuring, the second half quietly ruins the mood: the
router is doing fine, the relationship is not.

Only the standard library is used, and the bytes on disk never change
between runs.
"""

from pathlib import Path

NAME = "WiFi's fine. The marriage isn't."
TARGET = Path("/output") / "entry.txt"


def empty_folder(folder: Path) -> None:
    """Throw away everything inside folder, leaving folder standing."""
    folder.mkdir(parents=True, exist_ok=True)
    for item in folder.iterdir():
        if item.is_dir() and not item.is_symlink():
            _remove_tree(item)
        else:
            item.unlink()


def _remove_tree(folder: Path) -> None:
    for item in folder.iterdir():
        if item.is_dir() and not item.is_symlink():
            _remove_tree(item)
        else:
            item.unlink()
    folder.rmdir()


def run() -> None:
    # The count includes every byte in the file, so nothing extra may
    # sneak in after the last character -- no newline at the end.
    if len(NAME) != 32:
        raise SystemExit(f"expected 32 characters, found {len(NAME)}")
    empty_folder(TARGET.parent)
    TARGET.write_bytes(NAME.encode("utf-8"))
    # Read it back and make sure the disk holds exactly what we meant.
    saved = TARGET.read_bytes().decode("utf-8")
    if saved != NAME or len(saved) != 32:
        raise SystemExit("entry.txt does not hold the story")


if __name__ == "__main__":
    run()
