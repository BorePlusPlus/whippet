from pathlib import Path

from _pytest.capture import CaptureFixture

from tests import make_hooks_dir, assert_hooks_created
from whippet import __version__, whippet


def it_exposes_version():
    assert __version__ == "0.1.0"


def it_installs_hooks(tmp_path: Path) -> None:
    hooks_dir = make_hooks_dir(tmp_path)

    whippet.install_hooks(tmp_path)

    assert_hooks_created(hooks_dir)


def it_creates_hooks_dir_when_needed(tmp_path: Path) -> None:
    git_dir = tmp_path / ".git"
    git_dir.mkdir(parents=True)
    hooks_dir = git_dir / "hooks"
    assert not hooks_dir.exists()

    whippet.install_hooks(tmp_path)

    assert_hooks_created(hooks_dir)


def it_skips_installation_when_no_git_dir(
    tmp_path: Path, capsys: CaptureFixture
) -> None:
    whippet.install_hooks(tmp_path)
    captured = capsys.readouterr()
    hooks_dir = tmp_path / ".git" / "hooks"

    assert "skipping hooks installation" in captured.out
    assert not hooks_dir.exists()


def it_installs_hooks_in_git_dir_in_ancestor_dir(tmp_path: Path) -> None:
    hooks_dir = make_hooks_dir(tmp_path)
    cwd = tmp_path / "foo" / "bar"
    cwd.mkdir(parents=True)

    whippet.install_hooks(cwd)

    assert_hooks_created(hooks_dir)


def it_does_not_overwrite_existing_hooks(
    tmp_path: Path, capsys: CaptureFixture
) -> None:
    hooks_dir = make_hooks_dir(tmp_path)

    custom_hook = "Captain"
    custom_hook_path = hooks_dir / "pre-commit"
    custom_hook_path.write_text(custom_hook, encoding="utf-8")

    whippet.install_hooks(tmp_path)
    captured = capsys.readouterr()

    assert "pre-commit hook script already exists - skipping" in captured.out
    assert custom_hook_path.read_text(encoding="utf-8") == custom_hook

    assert_hooks_created(hooks_dir)
