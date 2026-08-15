"""Create a ZIP archive of a Python file or directory for grading.

Run this module from the root of a Python project. It bundles the requested file
or directory while excluding matching entries from the project's ``.gitignore``.

Example:
    python -m tools.submission [directory or file]
"""

import glob
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile

__author__ = ["Kris Jordan <kris@cs.unc.edu>", "Ezri White <ezri@live.unc.edu>"]


def main() -> None:
    """Build a timestamped submission archive from the CLI arguments.

    Files matching entries in the current directory's ``.gitignore`` are
    excluded from the archive.
    """
    target = parse_args()
    targeted = (
        expand_globs(".", target, {"**"})
        if os.path.isdir(target)
        else {expand_file(".", target)}
    )
    ignored = expand_globs(".", ".", readlines(".gitignore"))
    filtered = targeted.difference(ignored)
    if files_exist(filtered):
        create_zip(date_prefix(parse_file_string(target) + ".zip"), filtered)


def files_exist(files: set[str]) -> bool:
    """Check that every supplied file path exists.

    Args:
        files: Paths to validate.

    Returns:
        ``True`` when every path exists. In normal execution, a missing path
        exits the program rather than returning ``False``.

    Raises:
        SystemExit: If any path does not exist.
    """
    for path in files:
        if not Path(path).exists():
            print(
                "Error: Could not find file specified. Double check your spelling and punctuation."
            )
            sys.exit(1)
    return True


def parse_file_string(path: str) -> str:
    """Convert a path into a filesystem-safe portion of an archive name.

    Args:
        path: File or directory path to convert.

    Returns:
        The normalized relative path with path separators replaced by dashes.
    """
    normalized_path = expand_file(".", path)
    return normalized_path.replace(os.path.sep, "-")


def parse_args() -> str:
    """Read the submission target from the command-line arguments.

    Returns:
        The path of the directory or file to bundle.

    Raises:
        SystemExit: If no submission target is provided.
    """
    if len(sys.argv) < 2:
        print("Usage: python -m tools.submission [directory or .py file]")
        sys.exit(1)
    return sys.argv[1]


def readlines(path: str) -> set[str]:
    """Read nonempty, uncommented lines from a plaintext file.

    Inline comments beginning with ``#`` are removed, as is surrounding
    whitespace. Duplicate entries are collapsed into one set item.

    Args:
        path: Path of the plaintext file to read.

    Returns:
        The cleaned, unique lines, or an empty set if the file does not exist.
    """
    if not os.path.exists(path):
        return set()

    strip_comments_re = re.compile("#.+$")
    with open(path) as text_file:
        entries: set[str] = set()
        for line in text_file.read().splitlines():
            line = strip_comments_re.sub("", line).strip()
            if line != "":
                entries.add(line)
        return entries


def expand_globs(root: str, target: str, paths: set[str]) -> set[str]:
    """Expand glob patterns beneath a target and return paths relative to a root.

    Args:
        root: Root directory used to resolve inputs and relativize results.
        target: File or directory beneath ``root`` in which to expand patterns.
        paths: Glob patterns to expand beneath ``target``.

    Returns:
        A set of matching paths relative to ``root``.
    """
    entries: set[str] = set()
    abs_root: str = os.path.realpath(root)
    abs_target: str = os.path.realpath(os.path.join(abs_root, target))
    for path in paths:
        globbed_files = glob.glob(os.path.join(abs_target, path), recursive=True)
        for matched_path in globbed_files:
            file_path = matched_path.replace(f"{abs_root}{os.path.sep}", "")
            entries.add(file_path)
    return entries


def expand_file(root: str, target: str) -> str:
    """Normalize a target path relative to a root directory.

    Args:
        root: Root directory used to resolve and relativize ``target``.
        target: File or directory path to normalize.

    Returns:
        The normalized target path relative to ``root``.
    """
    abs_root: str = os.path.realpath(root)
    abs_target: str = os.path.realpath(os.path.join(abs_root, target))
    rel_path: str = abs_target.replace(f"{abs_root}{os.path.sep}", "")
    return rel_path


def filter_prefixes(source: set[str], filters: set[str]) -> set[str]:
    """Remove source paths that begin with any filtered prefix.

    Args:
        source: Paths to consider for inclusion.
        filters: Prefixes identifying paths to exclude.

    Returns:
        Source paths that do not begin with a filtered prefix.
    """
    return {
        path for path in source if not any(path.startswith(prefix) for prefix in filters)
    }


def create_zip(zip_path: str, files: set[str]) -> None:
    """Create a ZIP archive containing the supplied files.

    Args:
        zip_path: The path to the zip file to create.
        files: The set of files to add to the zip file created.
    """
    with ZipFile(zip_path, "w") as archive:
        for file in files:
            archive.write(file)


def date_prefix(suffix: str) -> str:
    """Prefix a suffix with the current local date and time.

    Args:
        suffix: Text to place after the timestamp and a dash.

    Returns:
        A string in the format ``YY.MM.DD-HH.MM.SS-{suffix}``.
    """
    now = datetime.now()
    prefix = (
        f"{str(now.year)[2:]}.{now.month:02}.{now.day:02}-"
        f"{now.hour:02}.{now.minute:02}.{now.second:02}"
    )
    return f"{prefix}-{suffix}"


if __name__ == "__main__":
    main()
