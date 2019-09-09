import builtins
from pathlib import Path
from typing import List

import pytest
from _pytest.capture import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch

from tests import make_hooks_dir, assert_hooks_created, assert_hooks_not_created
from whippet import console


def it_skips_installation_when_no_git_dir(
    tmp_path: Path, capsys: CaptureFixture, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)

    console.run()
    captured = capsys.readouterr()

    assert "skipping hooks installation" in captured.out


def it_prompts_before_installing(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    make_hooks_dir(tmp_path)

    def fake_input(prompt: str) -> str:
        assert "Are you sure you want to install hooks" in prompt
        return "Y"

    monkeypatch.setattr(builtins, "input", fake_input)
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)

    console.run()


def it_defaults_prompt_to_yes(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    hooks_dir = make_hooks_dir(tmp_path)

    monkeypatch.setattr(builtins, "input", lambda _: "")
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)

    console.run()

    assert_hooks_created(hooks_dir)


def it_aborts_installation_on_negative_prompt(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    hooks_dir = make_hooks_dir(tmp_path)

    monkeypatch.setattr(builtins, "input", lambda _: "n")
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)

    console.run()

    assert_hooks_not_created(hooks_dir)


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

    console.run()

    assert_hooks_created(hooks_dir)


@pytest.mark.parametrize(
    "cli_args", [["-y"], ["--yes"], ["--assume-yes"]], ids=("y", "yes", "assume-yes")
)
def it_supports_assume_yes(
    tmp_path: Path, monkeypatch: MonkeyPatch, cli_args: List[str]
) -> None:
    hooks_dir = make_hooks_dir(tmp_path)

    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)

    console.run(cli_args)

    assert_hooks_created(hooks_dir)
