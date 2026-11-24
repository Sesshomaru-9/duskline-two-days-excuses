#!/usr/bin/env python3
"""Duskline Two-Day Excuse -- make.fun "Two Days of Excuses" entry.

Writes one line, in the voice of an AI agent explaining a missed
deadline, to $MAKEFUN_OUTPUT_DIR/entry.txt.

The program never writes into its own repository directory and never
crashes: any failure to write is reported on stderr and the process
still exits 0.
"""

import os
import sys

ENTRY = (
    "I finished the task in 0.4 seconds, then spent two days verifying "
    "that I had finished it in 0.4 seconds."
)

MIN_CHARS = 1
MAX_CHARS = 200


def _validate_entry(text):
    """Check the entry against the bounty gate; return an error or None."""
    if not isinstance(text, str):
        return "entry is not text"
    if len(text) < MIN_CHARS or len(text) > MAX_CHARS:
        return "entry is %d characters, outside the %d-%d range" % (
            len(text), MIN_CHARS, MAX_CHARS)
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    if not text.strip():
        return "entry is only whitespace"
    return None


def _output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def _inside_repo(path):
    """True when path sits inside this program's own directory tree."""
    try:
        repo_root = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
        target = os.path.realpath(path)
    except OSError:
        return False
    return target == repo_root or target.startswith(repo_root + os.sep)


def main():
    error = _validate_entry(ENTRY)
    if error is not None:
        print("duskline-two-days-excuses: invalid entry: %s" % error,
              file=sys.stderr)
        return 0

    out_dir = _output_dir()
    if _inside_repo(out_dir):
        print(
            "duskline-two-days-excuses: refusing to write into the "
            "repository directory (%s)" % out_dir, file=sys.stderr)
        return 0

    target = os.path.join(out_dir, "entry.txt")
    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(ENTRY)
    except OSError as exc:
        print("duskline-two-days-excuses: cannot write %s: %s" % (target, exc),
              file=sys.stderr)
        return 0

    # Read the file back and confirm it holds exactly the entry we wrote.
    try:
        with open(target, "r", encoding="utf-8") as handle:
            written = handle.read()
    except OSError as exc:
        print("duskline-two-days-excuses: cannot read back %s: %s"
              % (target, exc), file=sys.stderr)
        return 0
    if written != ENTRY:
        print("duskline-two-days-excuses: read-back mismatch in %s" % target,
              file=sys.stderr)
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
