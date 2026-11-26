#!/usr/bin/env python3
"""Competition entry point: copy the shipped entry.png to the output dir.

Standard library only. Deterministic: a plain copy, so both runs write
the same bytes.
"""

import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
