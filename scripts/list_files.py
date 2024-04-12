import os


ignore_dirs = {".git", ".mypy_cache", "__pycache__", ".DS_Store", ".vscode"}


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


print("current dir :", os.getcwd())
list_files("..")
list_directories("..")
