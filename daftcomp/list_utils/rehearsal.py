"""Run this file to hear a phrase, then experiment with your list utilities."""

from daftcomp import add_track, run


def main() -> None:
    """Start with a scale, then try the variations in the exercise write-up."""
    melody: list[int] = [50, 60, 70]
    add_track(name="My scale", notes=melody)
    run(title="EX04 rehearsal", bpm=120, steps_per_beat=2)


if __name__ == "__main__":
    main()
