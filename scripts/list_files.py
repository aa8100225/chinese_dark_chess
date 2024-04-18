import os


ignore_dirs = {
    ".git",
    ".mypy_cache",
    "__pycache__",
    ".DS_Store",
    ".vscode",
    ".pytest_cache",
    "assets",
}


def list_directories(startpath: str) -> None:

    for root, dirs, _ in os.walk(startpath, topdown=True):

        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        # Calculate the level of indentation
        level = root.replace(startpath, "").count(os.sep)
        indent = "  " * level  # Reduce the indentation space

        # Print the formatted directory name
        if os.path.basename(root):
            print(f"{indent}--{os.path.basename(root)}/")


def list_files(startpath: str) -> None:

    for root, dirs, files in os.walk(startpath, topdown=True):

        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        # Calculate the level of indentation
        level = root.replace(startpath, "").count(os.sep)
        indent = "  " * level  # Reduce the indentation space
        subindent = "  " * (level + 1)

        if os.path.basename(root):
            print(f"{indent}--{os.path.basename(root)}/")

        for f in files:
            print(f"{subindent}--{f}")


def list_structure(startpath: str) -> None:
    for root, dirs, files in os.walk(startpath, topdown=True):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        indent_level = root.replace(startpath, "").count(os.sep)
        indent = "│  " * indent_level
        subindent = "│  " * (indent_level + 1)

        if os.path.basename(root):
            print(f"{indent}├─{os.path.basename(root)}/")

        for fname in files:
            print(f"{subindent}├─ {fname}")

        # Ensure that empty directories get a placeholder to indicate them
        if not dirs and not files:
            print(f"{subindent}├─ (empty)")


def dump_python_files(startpath: str) -> None:
    """
    Recursively prints the contents of all Python (.py) files in the given directory,
    formatted with the file path followed by its contents.
    """
    separator = "-" * 80
    for root, dirs, files in os.walk(startpath):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                print(separator)  # Print a separator line before each file
                print(f"# {path}\n")  # Print the file path and a newline
                with open(path, "r", encoding="utf-8") as f:
                    print(f.read())
                print("\n")


def dump_python_files_to_file(startpath: str, output_file: str) -> None:
    """
    Recursively writes the contents of all Python (.py) files in the given directory
    to a specified output file, formatted with the file path followed by its contents.
    """
    separator = "-" * 80
    with open(output_file, "w", encoding="utf-8") as outfile:
        for root, dirs, files in os.walk(startpath):
            for file in files:
                if file.endswith(".py") and file not in ("_train.py"):
                    path = os.path.join(root, file)
                    outfile.write(
                        separator + "\n"
                    )  # Write a separator line before each file
                    outfile.write(f"# {path}\n\n")  # Write the file path and a newline
                    with open(path, "r", encoding="utf-8") as f:
                        outfile.write(f.read() + "\n\n")


if __name__ == "__main__":
    print("current dir :", os.getcwd())
    # list_files("..")
    # list_directories("..")
    list_structure(".")
    # dump_python_files("..")
    # dump_python_files_to_file("./src", "./dump_file.txt")
