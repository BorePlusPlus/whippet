from whippet import whippet
from pathlib import Path


def run():
    cwd = Path.cwd()
    git_dir = whippet.resolve_git_dir(cwd)
    if git_dir is None:
        print("whippet - Can not find .git directory, skipping hooks installation.")
        return

    while True:
        answer = input(
            f"whippet - Are you sure you want to install hooks in {git_dir}? [Y/n]"
        ).lower()
        if answer == "n":
            print("whippet - Aborted.")
            return
        if answer in ["y", ""]:
            break

    whippet.install_hooks(cwd)
