# Workspace support

`sync.py` prepares and checks every Python project in this VS Code workspace.

## First-time setup

- [Set up on macOS](SETUP_MAC.md)
- [Set up on Windows](SETUP_WINDOWS.md)

## Run it

1. In VS Code, select **Terminal > Run Task**.
2. Select **Sync all workspace projects** for the `support` folder.
3. Follow the messages in the terminal.

You can also run it from a terminal:

```console
uv run --managed-python sync.py
```

The first run may take a few minutes while uv downloads Python and project
dependencies. Later runs are usually much faster, and it is always safe to run
the script again.

## What it checks

For every sibling folder containing a `pyproject.toml`, the script:

- first fetches updates from Git's `origin`, previews the merge with
  `git merge-tree`, and only applies the update when Git predicts a
  conflict-free result;
- detects virtual environments that still contain an absolute path from before
  the workspace was moved or renamed, then recreates them automatically in
  uv's relocatable mode;
- runs `uv sync --locked --managed-python` so macOS and Windows both install
  from the same committed, cross-platform lockfile without rewriting it;
- checks the installed packages for dependency conflicts;
- parses project-owned Python files for syntax errors;
- validates Jupyter notebooks as JSON; and
- runs recognizable Python tests, with a 60-second limit, when tests exist.

Student setup deliberately does not upgrade locked packages. When course
maintainers want newer dependency versions, they can run `uv lock --upgrade`
in the relevant project, review the resulting `uv.lock`, and commit it for every
student to receive through the normal workspace update.

The script itself depends only on Python's standard library and declares its
Python requirement as inline uv script metadata. It expects
[`uv`](https://docs.astral.sh/uv/) to be installed and available on `PATH`, but
does not require a system Python or a virtual environment for the `support`
folder. uv downloads a compatible managed Python automatically when necessary.
