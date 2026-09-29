"""Run as a module or directly from your editor after implementing scale_range."""

import sys
from pathlib import Path

# Keep list_utils imports working with VS Code's Run Python File button.
if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from daftcomp import add_track, run


def main() -> None:
    """Start with a scale, then try the variations in the exercise write-up."""
    melody: list[int] = [50, 60, 70]
    add_track(name="My scale", notes=melody)
    run(title="EX04 rehearsal", bpm=120, steps_per_beat=2)


if __name__ == "__main__":
    main()
