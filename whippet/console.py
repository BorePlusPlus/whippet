from whippet import whippet
from pathlib import Path


def install_prompt(git_dir: Path) -> bool:
    while True:
        answer = input(
            f"whippet - Are you sure you want to install hooks in {git_dir}? [Y/n] "
        ).lower()
        if answer == "n":
            return False
        if answer in ["y", ""]:
            return True


def run():
    cwd = Path.cwd()
    git_dir = whippet.resolve_git_dir(cwd)

    if git_dir is None:
        print("whippet - Can not find .git directory, skipping hooks installation.")
        return

    if not install_prompt(git_dir):
        print("whippet - Aborted.")
        return

    whippet.install_hooks(cwd)
