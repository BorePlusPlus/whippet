from pathlib import Path

from whippet import whippet


def make_hooks_dir(path: Path) -> Path:
    hooks_dir = path / ".git" / "hooks"
    hooks_dir.mkdir(parents=True)
    return hooks_dir


def assert_hooks_created(hooks_dir: Path) -> None:
    for hook in whippet.hook_list:
        hook_path = hooks_dir / hook
        assert hook_path.exists()
        assert hook_path.is_file()


def assert_hooks_not_created(hooks_dir: Path) -> None:
    assert list(hooks_dir.glob("*")) == []
