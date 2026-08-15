# Set up the COMP110 workspace on macOS

This guide covers the complete setup of a Mac for COMP110. When you finish, you
will have the course workspace open in Visual Studio Code and be ready to run
Python programs.

## What you are installing

The setup has three tools with different jobs:

- **Git** downloads the course repository and records changes to its files.
- **Visual Studio Code** is the editor in which you will read, write, and run
  code.
- **uv** installs Python and the course software packages needed to run
  programs.

These tools work together: Git obtains the course files, VS Code provides a
place to work with them, and uv prepares the software needed to run them.

You will need an internet connection and macOS 13 or newer. If a tool is already installed and its verification command succeeds, continue to the next section.

## 1. Learn where commands run

Open **Terminal**:

1. Press **Command+Space** to open Spotlight Search.
2. Type `Terminal`.
3. Press **Return**.

The terminal is a text interface to your computer. A command is an instruction
entered after the prompt. In this guide, copy only the text inside each code
block, paste it into Terminal, and press **Return**.

## 2. Install Git

First, ask whether Git is already available:

```console
git --version
```

If the command prints a version such as `git version 2.39.5`, Git is ready.

If macOS offers to install Command Line Developer Tools, select **Install** and
accept the license. These tools include Git. If no installation dialog appears,
start it explicitly:

```console
xcode-select --install
```

After the installation finishes, verify Git again:

```console
git --version
```

You should see a version print out. This is the macOS installation method documented by the
[official Git project](https://git-scm.com/install/mac.html). If you run into difficulty, try referring to the [official `git` website](https://git-scm.com/install/mac.html).

## 3. Install Visual Studio Code

Follow Microsoft's
[official VS Code instructions for macOS](https://code.visualstudio.com/docs/setup/mac):

1. Download [Visual Studio Code for macOS](https://code.visualstudio.com/Download).
   The Universal build works on both Apple silicon and Intel Macs.
2. Open the downloaded `.dmg` file.
3. Drag **Visual Studio Code.app** into **Applications**.
4. In Finder, find the **Visual Studio Code** disk under **Locations** in the
   sidebar and click the eject button beside it.
5. Open **Downloads** in Finder and move the Visual Studio Code `.dmg` file to
   the Trash.

These cleanup steps ensure that future launches use the installed application
in **Applications**, rather than the temporary copy on the disk image.

## 4. Install uv

Return to Terminal and run Astral's official standalone installer:

```console
curl -LsSf https://astral.sh/uv/install.sh | sh
```

The shell syntax in this command is beyond the scope of this guide. At a high
level, it downloads and runs the uv installer from Astral, the developer of uv.
The command comes from the
[official uv installation guide](https://docs.astral.sh/uv/getting-started/installation/),
which also explains how to inspect the script before running it.

When the installer finishes, read its final messages. It may tell you that it
updated your shell configuration or give you a command to update the current
terminal. Completely quit Terminal (**Command+Q**), then reopen it. This gives
the new Terminal process a fresh view of your `PATH`: the list of locations
where macOS looks for commands.

Verify uv:

```console
uv --version
```

A successful result begins with `uv`, followed by a version number. A later
workspace setup step will ask uv to prepare Python and the course packages.

## 5. Clone the course repository

In this context, **clone** means “make a local copy of the repository, including
its version history.” Keep the repository in a stable location rather than in
Downloads. Create a `code` folder in your home folder:

```console
mkdir -p "$HOME/code"
```

Here, `$HOME` means your user home directory, usually
`/Users/your-username`. This command creates the `code` folder inside it.

Now clone through Visual Studio Code, following its
[official repository-cloning workflow](https://code.visualstudio.com/docs/sourcecontrol/repos-remotes#_clone-repositories):

1. Open Visual Studio Code from **Applications**. macOS might ask whether you
   want to open an application downloaded from the internet. Confirm.
2. Press **Command+Shift+P** to open the Command Palette.
3. Type and select **Git: Clone**.
4. Paste the public course repository URL into the prompt and press **Return**:

   ```text
   https://github.com/comp110-26f/comp110-26f-workspace.git
   ```

5. When asked where to place the repository, select the `code` folder you just
   created inside your user home directory. In the folder chooser, you can press
   **Command+Shift+H** to open your home directory, then select `code`. Git
   creates `comp110-26f-workspace` inside it.
6. Select **Open** when cloning finishes.

If VS Code cannot find the repository, check the internet connection and confirm
that the URL matches the one above.

## 6. Open the course workspace

The `workspace.code-workspace` file opens the student-facing project and
support folders together in one VS Code window.

1. Select **File > Open Workspace from File…**.
2. Open `workspace.code-workspace` from the cloned repository.
3. If VS Code asks whether you trust the workspace authors, confirm that the
   path is your course repository and select **Yes, I trust the authors**.
4. VS Code may display this notification or message in the Source Control view:
   **A Git repository was found in the parent folders of the workspace or the
   open file(s).** Select **Open Repository**, then select
   `comp110-26f-workspace` if VS Code asks you to choose a repository.

Trust allows the repository's tasks, settings, debugging configuration, and
extensions to run. VS Code intentionally restricts those features for unknown
code; see Microsoft's
[Workspace Trust documentation](https://code.visualstudio.com/docs/editing/workspaces/workspace-trust).

The repository message appears because the workspace shows the course's
project folders while Git tracks the surrounding `comp110-26f-workspace`
folder. Opening it gives VS Code access to Git features for the complete course
repository; it does not replace the workspace you just opened. Microsoft's
[Source Control FAQ](https://code.visualstudio.com/docs/sourcecontrol/faq#_why-isnt-vs-code-discovering-git-repositories-in-parent-folders-of-workspaces-or-open-files)
explains this parent-folder behavior.

The Explorer should now show `trailhead` and `support` as separate top-level
folders. The title bar at the top of the VS Code window should include
**COMP110 26F Workspace**. If that text is missing or the Explorer shows only
one repository folder, reopen the `.code-workspace` file rather than the folder
containing it.

## 7. Install the recommended extensions

When VS Code offers to install recommended extensions for the workspace, select
**Install** or **Install All**. The recommendations include Python language
support, the Python debugger, Jupyter notebook support, Pylance, and Ruff.

If the notification does not appear:

1. Select the Extensions icon in the Activity Bar on the far left. It looks like
   four small blocks, with one block separated from the other three. Hover over
   it to see the label **Extensions**. You can also press
   **Command+Shift+X**.
2. Type `@recommended` in the search box.
3. Install the recommendations under **Workspace Recommendations**.

Extensions add language-aware editing, running, debugging, notebook, and code
quality features to VS Code.

## 8. Prepare the workspace

Run the workspace's setup task:

1. Select **Terminal > Run Task…**.
2. Select **Sync all workspace projects** for the `support` folder.
3. Watch the terminal output. The first run can take a few minutes because uv
   downloads Python and project packages.

The task runs this command from the `support` folder:

```console
uv run --managed-python sync.py
```

The command's details are beyond the scope of this guide. At a high level, it
asks uv to run the course setup script using Python managed by uv. The script
checks the public repository for newer course files, finds the course projects,
installs the software they need, and performs basic checks.

Setup succeeds when the output reaches **Workspace setup summary**, reports
`[OK]` for every project, and ends with:

```text
Everything is ready. You can start working!
```

It is safe to run the task again. If the workspace is moved or renamed, running
the task again repairs the generated setup files.

## 9. Confirm the setup after restarting VS Code

First, confirm that VS Code can reopen the complete course workspace:

1. Completely quit VS Code (**Command+Q**).
2. Reopen Visual Studio Code from **Applications**.
3. Select **File > Open Recent**.
4. Select the recent item for this course whose name ends in **(Workspace)**.
5. Check that the title bar includes **COMP110 26F Workspace** and that the
   Explorer shows `trailhead` and `support`.

Next, run the welcome program directly:

1. In the Explorer, expand `trailhead` and open `hello.py`.
2. Select the triangular **Run Python File** button in the upper-right corner of
   the editor.
3. Confirm that a terminal opens, the program prints its output, and no error
   traceback appears.

Finally, start Trailhead through VS Code:

1. Select the **Run and Debug** icon in the Activity Bar on the far left. It
   looks like a play triangle with a small bug.
2. At the top of the Run and Debug pane, select **Trailhead: Debug Server**.
3. Select the green **Start Debugging** triangle, or press **F5**.
4. Open <http://127.0.0.1:1110> in a web browser. The Trailhead page should
   load.
5. In Trailhead, run `hello.py` and confirm that its output appears.
6. Return to VS Code and stop Trailhead with the red square in the debug toolbar
   (**Shift+F5**).

Congratulations—your COMP110 development workspace is ready. You installed and
connected Git, VS Code, uv, and Python; cloned a version-controlled codebase;
added language and debugging tools to your editor; and verified that you can run
and debug a program. You have assembled a modern development workflow using
leading free tools and open-source technologies—the same foundations used by
professional software developers.

## Troubleshooting

### `git: command not found`

Run `xcode-select --install`, finish the installation, and open a new Terminal.
Then run `git --version` again.

### `uv: command not found`

Completely quit Terminal and VS Code (**Command+Q** in each application), then
reopen them. Run `uv --version` in Terminal. If it still fails, rerun the
installer and follow the exact `PATH` instruction printed at the end.

### **Git: Clone** is missing or VS Code cannot find Git

Verify `git --version` in Terminal, then completely quit VS Code
(**Command+Q**) and reopen it. VS Code discovers Git when the application
starts.

### The setup task is missing

Confirm the Explorer shows `trailhead` and `support` as top-level folders. If
not, use **File > Open Workspace from File…** and open
`workspace.code-workspace`.

### A Python download or package installation fails

Read the first `[FAIL]` message in the task output. Check the internet
connection, reconnect to any required campus network or VPN, and run the task
again. Save the complete terminal output if you need course support.

## Official references

- [Install Git on macOS](https://git-scm.com/install/mac.html)
- [Install Visual Studio Code on macOS](https://code.visualstudio.com/docs/setup/mac)
- [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Install and manage Python with uv](https://docs.astral.sh/uv/guides/install-python/)
- [Clone repositories in Visual Studio Code](https://code.visualstudio.com/docs/sourcecontrol/repos-remotes#_clone-repositories)
- [Use extensions in Visual Studio Code](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace)
- [Open a recent workspace](https://code.visualstudio.com/docs/editing/tips-and-tricks#_navigate-between-recently-opened-folders-and-workspaces)
- [Run Python code in Visual Studio Code](https://code.visualstudio.com/docs/languages/python#_run-python-code)
- [Debug code in Visual Studio Code](https://code.visualstudio.com/docs/debugtest/debugging)
