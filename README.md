# Python Shell Implementation

This is a simple shell implementation written in Python that provides basic command-line functionality similar to Unix/Linux shells. It supports built-in commands, external command execution, and basic output redirection.

## Features

- **Built-in Commands**:
  - `pwd`: Print working directory
  - `cd`: Change directory
  - `echo`: Print arguments to stdout
  - `type`: Display command type (builtin or executable path)
  - `exit`: Exit the shell

- **External Command Execution**:
  - Searches `PATH` for executable commands
  - Executes external programs with argument support

- **Output Redirection**:
  - Support for `>` (overwrite) and `>>` (append) operators
  - Handles stdout redirection (`>`, `>>`, `1>`, `1>>`)
  - Handles stderr redirection (`2>`, `2>>`)

## Usage

Run the shell by executing:

```bash
python main.py
```

```bash
$ pwd /current/working/directory
$ echo Hello World > output.txt
$ cd ~
$ type echo
echo is a shell builtin
```

## Implementation Details

* `generate_prompt()`: Displays the shell prompt
* `is_command_builtin()`: Checks if a command is a built-in shell command
* `change_directory()`: Handles directory navigation with error handling
* `find_executable()`: Searches `PATH` for external commands
* `main()`: Main loop that processes commands and handles redirections

## Error Handling

* Invalid command syntax
* File/directory not found
* Permission errors
* Invalid redirection
