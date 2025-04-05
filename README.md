# Python Microshell Reference (for 42 Minishell/Microshell)

## Overview

This Python script implements a very basic command-line interpreter, similar in concept to the `microshell` exercise from the 42 exams, which itself is a simplified version of the `minishell` project.

**Purpose:** This script is intended as a **learning tool and reference** to understand the core logic and system interactions required for the C version. It demonstrates concepts like process creation, command execution, built-in commands, and signal handling using Python's `os` and `signal` modules, which often wrap the underlying C system calls.

## Features Implemented (in this Python version)

- **Command Prompt:** Displays a `$` prompt and reads user input.
- **Basic Parsing:** Splits input line into command and arguments using `.split()`.
- **External Command Execution:**
	- Uses `os.fork()` to create a child process.
	- Uses `os.execvp()` in the child to replace its image with the requested command (searches `PATH`).
	- Uses `os.waitpid()` in the parent to wait for the child to complete.
- **Built-in `cd` Command:**
	- Handles `cd` directly in the parent process using `os.chdir()`.
	- Includes error handling for incorrect arguments (`error: cd: bad arguments`) and execution failures (`error: cd: cannot change directory to ...`) as per the spec.
- **Signal Handling:**
	- **CTRL+C (`SIGINT`):** Catches `KeyboardInterrupt` at the prompt to show a new prompt. Child processes are terminated by default. Parent prints a newline when child is terminated by `SIGINT`.
	- **CTRL+\ (`SIGQUIT`):** The parent shell ignores `SIGQUIT`. Child processes are terminated by default (and may dump core). Parent prints "Quit" when child is terminated by `SIGQUIT`.
	- **CTRL+D (`EOF`):** Catches `EOFError` to gracefully exit the shell.
- **Error Handling:**
	- Handles empty input lines.
	- Handles `execvp` failures (e.g., command not found, permissions) with `error: cannot execute ...`.
	- Handles `fork` and `waitpid` failures with `error: fatal`.
	- Child process exits correctly (`os._exit(1)`) upon `execvp` failure.

## How to Run

1.  Save the code as a Python file (e.g., `pymicroshell.py`).
2.  Make sure you have Python 3 installed.
3.  Run from your terminal:
    ```bash
    python pymicroshell.py
    ```