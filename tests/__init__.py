import stat
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
        assert stat.S_IMODE(hook_path.stat().st_mode) == 0o775


def assert_no_hooks(hooks_dir: Path) -> None:
    assert list(hooks_dir.glob("*")) == []
