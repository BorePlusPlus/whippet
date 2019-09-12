import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import List, Tuple, Optional

from whippet import whippet


def prompt(action: str, git_dir: Path) -> bool:
    while True:
        answer = input(
            f"whippet - Are you sure you want to {action} hooks in {git_dir}? [Y/n] "
        ).lower()
        if answer == "n":
            return False
        if answer in ["y", ""]:
            return True


def get_dirs() -> Tuple[Path, Optional[Path]]:
    cwd = Path.cwd()
    git_dir = whippet.resolve_git_dir(cwd)
    return cwd, git_dir


def make_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="whippet", description="Install make based git hooks with ease."
    )
    parser.add_argument(
        "command",
        choices=["install", "uninstall"],
        default="install",
        nargs="?",
        help="Install or uninstall whippet managed git hooks.",
    )
    parser.add_argument(
        "-y",
        "--yes",
        "--assume-yes",
        action="store_true",
        help='Automatic yes to prompts; assume "yes" as answer to all prompts and run non-interactively.',
    )
    return parser


def install(args: Namespace) -> None:
    cwd, git_dir = get_dirs()

    if git_dir is None:
        print("whippet - Can not find .git directory, skipping hooks installation.")
        return

    if not (args.yes or prompt("install", git_dir)):
        print("whippet - Aborted.")
        return

    whippet.install_hooks(cwd)


def uninstall(args: Namespace) -> None:
    cwd, git_dir = get_dirs()

    if git_dir is None:
        print("whippet - Can not find .git directory, skipping hooks uninstallation.")
        return

    if not (args.yes or prompt("uninstall", git_dir)):
        print("whippet - Aborted.")
        return

    whippet.uninstall_hooks(cwd)


def run(cli_args: List[str]) -> None:
    args = make_parser().parse_args(args=cli_args)

    globals()[args.command](args)


def main() -> None:
    run(sys.argv[1:])
