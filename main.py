import sys
import os
import subprocess
import shlex

def generate_prompt():
    sys.stdout.write("$ ")
    sys.stdout.flush()

def is_command_builtin(command):
    return command in builtins

def change_directory(path):
    home = os.environ.get("HOME", "")
    try:
        if path == "~":
            os.chdir(home)
        else:
            os.chdir(path)
        return ""
    except FileNotFoundError:
        return f"{path}: No such file or directory"
    except NotADirectoryError:
        return f"{path}: Not a directory"
    except PermissionError:
        return f"{path}: Permission denied"

def find_executable(command):
    path = os.environ.get("PATH", "")
    for directory in path.split(os.pathsep):
        file_path = os.path.join(directory, command)
        if os.access(file_path, os.X_OK):
            return file_path
    return None

builtins = ["exit", "echo", "type", "pwd", "cd"]

def main():
    while True:
        generate_prompt()
        try:
            command_args = shlex.split(input())
        except ValueError as e:
            print(f"Error parsing command: {e}", file=sys.stderr)
            continue

        if not command_args:
            continue

        command = command_args[0]
        arguments = command_args[1:]
        rdo = None
        outfile_path = None
        append_mode = False
        stderr_redirect = False

        # Detect redirection operators
        if len(arguments) >= 3 and arguments[-2] in [">", "1>", "2>", ">>", "1>>", "2>>"]:
            rdo = arguments[-2]
            outfile_path = arguments[-1]
            append_mode = rdo in ["1>>", ">>", "2>>"]
            stderr_redirect = rdo.startswith("2")
            arguments = arguments[:-2]

        out, err = "", ""

        # Check if the command is a builtin
        is_builtin = is_command_builtin(command)

        # Handle commands
        match command:
            case "pwd":
                out = f"{os.getcwd()}"
            case "cd":
                if arguments:
                    out = change_directory(arguments[0])
                else:
                    out = "cd: missing argument"
            case "type":
                if arguments:
                    path = find_executable(arguments[0])
                    if is_command_builtin(arguments[0]):
                        out = f"{arguments[0]} is a shell builtin"
                    elif path:
                        out = f"{arguments[0]} is {path}"
                    else:
                        out = f"{arguments[0]}: not found"
                else:
                    out = "type: missing argument"
            case "echo":
                out = " ".join(arguments)
            case "exit":
                if not arguments or arguments[0] == "0":
                    sys.exit()
                else:
                    print(f"exit: invalid argument: {arguments[0]}")
            case _:
                executable = find_executable(command)
                if executable:
                    result = subprocess.run(
                        [command] + arguments,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )
                    out = result.stdout.rstrip()
                    err = result.stderr.rstrip()
                else:
                    out = f"{command}: command not found"

        # Handle redirection
        if rdo:
            mode = "a" if append_mode else "w"
            try:
                with open(outfile_path, mode) as file:
                    if stderr_redirect:  # Handle 2>> operator
                        if err:  # Only write if there's actual error content
                            file.write(err + "\n")
                        err = ""
                    else:
                        if out:  # Only write if there's actual output
                            file.write(out + "\n")
                        out = ""
            except OSError as e:
                err = f"{outfile_path}: {e}"
        # Print errors and output
        if err:
            print(err, file=sys.stderr)
        if out:
            print(out)

if __name__ == "__main__":
    main()