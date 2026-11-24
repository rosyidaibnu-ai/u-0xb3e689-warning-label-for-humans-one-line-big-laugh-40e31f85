#!/usr/bin/env python3
"""Warning Label for Humans: One Line, Big Laugh — entry program.

Writes a single original warning-label line (157 characters) to
/output/entry.txt: the safety warning that should come printed on every
human being. The line is written from scratch for this bounty; it copies
no other entry and no existing text.
"""

import os
import sys
from pathlib import Path

# One original line (157 characters): a printed safety label for the
# contents of every human — handle with snacks. The side effects are the
# joke, and the last few words land it: the label quotes the human
# replying to a question nobody asked.
ENTRY = (
    "WARNING: Contents: one (1) human. Handle with snacks. Side effects: "
    "strong opinions, unfinished sentences, and 'per my last email' "
    "to questions nobody asked."
)

# Output path: overridable for local testing via MAKEFUN_OUTPUT_PATH.
OUTPUT_PATH = Path(os.environ.get("MAKEFUN_OUTPUT_PATH", "/output/entry.txt"))

MIN_LENGTH = 1
MAX_LENGTH = 160


def validate_entry(text: str) -> str:
    """Check the text is one line the gate will accept."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(text) < MIN_LENGTH or len(text) > MAX_LENGTH:
        raise ValueError(
            f"entry is {len(text)} chars, outside the 1-160 char range"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def write_entry(entry: str, path: Path) -> None:
    """Write the entry directly to its destination, world-readable.

    Writes straight to the target file (no temp file is ever created in
    the output directory) and sets mode 0644 explicitly, so the grader
    can read the file whoever runs it.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(entry)
        fh.flush()
        os.fsync(fh.fileno())
    os.chmod(path, 0o644)


def main() -> int:
    try:
        entry = validate_entry(ENTRY)
    except ValueError as exc:
        print(f"error: invalid entry: {exc}", file=sys.stderr)
        return 2
    try:
        write_entry(entry, OUTPUT_PATH)
        written = OUTPUT_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: cannot write {OUTPUT_PATH}: {exc}", file=sys.stderr)
        return 3
    if written != entry:
        print(
            "error: round-trip check failed: file does not hold the entry",
            file=sys.stderr,
        )
        return 4
    print(f"wrote {len(written)}-char entry to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
