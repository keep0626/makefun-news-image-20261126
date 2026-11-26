"""Thursday 26 November 2026 — the world in one page.

This module is the submission entry point for the world-news poster
dated Thursday 26 November 2026. Its job is deliberately tiny: take
the finished poster, entry.png, which lives in the same folder as
this file, and place a faithful copy of it in the output directory.

Nothing here draws, edits, or re-encodes the image. The copy is a
straight byte-for-byte transfer, so running this entry point twice
leaves two outputs whose bytes match exactly.
"""

from __future__ import annotations

import os
from pathlib import Path


def deliver_finished_poster() -> Path:
    """Carry entry.png from this folder into the output directory."""
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "entry.png"
    destination.write_bytes(source.read_bytes())
    print(f"Copied {source} to {destination}")
    return destination


if __name__ == "__main__":
    deliver_finished_poster()
