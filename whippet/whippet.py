from pathlib import Path
from typing import Optional, List

from whippet import __version__

hook_list: List[str] = [
    "applypatch-msg",
    "pre-applypatch",
    "post-applypatch",
    "pre-commit",
    "prepare-commit-msg",
    "commit-msg",
    "post-commit",
    "pre-rebase",
    "post-checkout",
    "post-merge",
    "pre-push",
    "pre-receive",
    "update",
    "post-receive",
    "post-update",
    "push-to-checkout",
    "pre-auto-gc",
    "post-rewrite",
    "sendemail-validate",
]


def resolve_git_dir(cwd: Path) -> Optional[Path]:
    cwd = cwd.resolve()
    while True:
        git_dir = cwd / ".git"
        if git_dir.exists() and git_dir.is_dir():
            return git_dir
        if cwd == cwd.parent:
            return None
        cwd = cwd.parent


def get_hooks_dir(cwd: Path) -> Optional[Path]:
    git_dir = resolve_git_dir(cwd)
    if git_dir is None:
        return None

    hook_dir = git_dir / "hooks"
    hook_dir.mkdir(mode=0o775, exist_ok=True)
    return hook_dir


def install_hooks(cwd: Path) -> None:
    hooks_dir = get_hooks_dir(cwd)
    if hooks_dir is None:
        print("whippet - Can not find .git directory, skipping hooks installation.")
        return

    template_path = Path(__file__).parent / "hook_template"
    template = template_path.read_text(encoding="utf-8")

    for hook_name in hook_list:
        hook_file = hooks_dir / hook_name
        # if hook_file.exists():
        #     print(f"{hook_name} hook script already exists - ")
        hook = template.format(version=__version__, hook=hook_name)
        hook_file.write_text(hook, encoding="utf-8")
