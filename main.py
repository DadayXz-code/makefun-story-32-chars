#!/usr/bin/env python3
"""Tell a Whole Story in 32 Characters.

Writes a single Wi-Fi network name of exactly 32 characters to
/output/entry.txt. The name is a whole story in miniature: the setup
("WiFi's fine") promises everything is okay, then the punchline
("The marriage isn't") flips it -- a household where the internet
outlasted the relationship.

Standard library only. Deterministic: every run writes the same bytes.
"""

import os
import shutil

STORY = "WiFi's fine. The marriage isn't."

OUTPUT_DIR = "/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "entry.txt")


def main() -> int:
    # The gate counts every character in the file, so the text is written
    # with no trailing newline: exactly 32 characters, nothing more.
    assert len(STORY) == 32, f"story must be 32 characters, got {len(STORY)}"

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Clear the output directory's contents without deleting /output itself.
    for child in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, child)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as handle:
        handle.write(STORY)

    # Verify what actually landed on disk: the gate rejects anything
    # that is not 1-32 characters, so a stray newline would sink the entry.
    with open(OUTPUT_FILE, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    assert written == STORY, "output does not match the story"
    assert len(written) == 32, f"output must be 32 characters, got {len(written)}"

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
