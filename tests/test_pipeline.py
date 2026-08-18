from pathlib import Path
import shutil
import subprocess

import pytest

from esm2_fitness.pipeline import main


def test_check_command_is_lightweight_and_offline(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = main(["check"])

    assert result == 0
    assert "offline" in capsys.readouterr().out
    assert list(tmp_path.iterdir()) == []


def test_synthetic_command_uses_only_small_local_fixture(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = main(["synthetic"])

    assert result == 0
    assert "synthetic" in capsys.readouterr().out
    assert list(tmp_path.iterdir()) == []


def test_real_command_fails_closed_without_explicit_flag(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = main(["real"])

    output = capsys.readouterr().out
    assert result == 2
    assert '"status": "skipped"' in output
    assert "allow-external-data" in output
    assert not Path("results_public").exists()


def test_bash_wrapper_runs_the_lightweight_check():
    bash = shutil.which("bash")
    if bash is None:
        pytest.skip("bash is not available on this host")

    repository = Path(__file__).parents[1]
    completed = subprocess.run(
        [bash, "run.sh", "check"],
        cwd=repository,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "offline" in completed.stdout
