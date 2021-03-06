import builtins
from pathlib import Path

import pytest
from _pytest.capture import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch

from tests import make_hooks_dir, assert_hooks_created, assert_no_hooks
from whippet import console


def it_installs(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    hooks_dir = make_hooks_dir(tmp_path)

    monkeypatch.setattr(builtins, "input", lambda _: "Y")
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)

    console.run(["install"])

    assert_hooks_created(hooks_dir)


def it_defaults_command_to_install(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    hooks_dir = make_hooks_dir(tmp_path)

    monkeypatch.setattr(builtins, "input", lambda _: "Y")
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)

    console.run([])

    assert_hooks_created(hooks_dir)


def it_skips_installation_when_no_git_dir(
    tmp_path: Path, capsys: CaptureFixture, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)

    console.run(["install"])
    captured = capsys.readouterr()

    assert "skipping hooks installation" in captured.out


def it_prompts_before_installing(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    make_hooks_dir(tmp_path)

    def fake_input(prompt: str) -> str:
        assert "Are you sure you want to install hooks" in prompt
        return "Y"

    monkeypatch.setattr(builtins, "input", fake_input)
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)

    console.run(["install"])


def it_defaults_prompt_to_yes(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    hooks_dir = make_hooks_dir(tmp_path)

    monkeypatch.setattr(builtins, "input", lambda _: "")
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)

    console.run(["install"])

    assert_hooks_created(hooks_dir)


def it_aborts_installation_on_negative_prompt(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    hooks_dir = make_hooks_dir(tmp_path)

    monkeypatch.setattr(builtins, "input", lambda _: "n")
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)

    console.run(["install"])

    assert_no_hooks(hooks_dir)


def it_keeps_prompting_until_given_acceptable_answer(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    hooks_dir = make_hooks_dir(tmp_path)
    attempts = 5

    def fake_input(_: str) -> str:
        nonlocal attempts
        attempts -= 1
        return "x" * attempts

    monkeypatch.setattr(builtins, "input", fake_input)
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)

    console.run(["install"])

    assert_hooks_created(hooks_dir)


@pytest.mark.parametrize("yes_arg", ["-y", "--yes", "--assume-yes"])
def it_supports_assume_yes(
    tmp_path: Path, monkeypatch: MonkeyPatch, yes_arg: str
) -> None:
    hooks_dir = make_hooks_dir(tmp_path)

    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)

    console.run(["install", yes_arg])

    assert_hooks_created(hooks_dir)


def it_uninstalls(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    hooks_dir = make_hooks_dir(tmp_path)
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)
    console.run(["install", "-y"])
    assert_hooks_created(hooks_dir)

    console.run(["uninstall", "-y"])

    assert_no_hooks(hooks_dir)
