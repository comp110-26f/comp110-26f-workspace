"""Launch the provided chat runtime using src/decoders student code."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from chat110.cli import main

if __name__ == "__main__":
    main()
