from argparse import ArgumentParser
from typing import List, Optional

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


def make_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="whippet", description="Install make based hooks with ease."
    )
    parser.add_argument(
        "-y",
        "--yes",
        "--assume-yes",
        action="store_true",
        help='Automatic yes to prompts; assume "yes" as answer to all prompts and run non-interactively.',
    )
    return parser


def run(cli_args: Optional[List[str]] = None) -> None:
    cwd = Path.cwd()
    git_dir = whippet.resolve_git_dir(cwd)

    if git_dir is None:
        print("whippet - Can not find .git directory, skipping hooks installation.")
        return

    args = make_parser().parse_args(args=cli_args)

    if not (args.yes or install_prompt(git_dir)):
        print("whippet - Aborted.")
        return

    whippet.install_hooks(cwd)


def main() -> None:
    run([])
