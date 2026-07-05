"""Shared fixtures for the end-to-end (integration) test suite."""

import filecmp
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

ASSETS_DIR = Path(__file__).parent.parent.parent / "test-assets"
SOURCE_DIR = ASSETS_DIR / "source"
EXPECTED_DIR = ASSETS_DIR / "expected"


def _assert_trees_equal(expected: Path, actual: Path) -> None:
    """Assert two directory trees are byte-identical (structure + file content)."""
    cmp = filecmp.dircmp(expected, actual)
    _assert_dircmp(cmp, expected, actual)


def _assert_dircmp(cmp: filecmp.dircmp, expected: Path, actual: Path) -> None:
    assert not cmp.left_only, f"missing from output under {actual}: {sorted(cmp.left_only)}"
    assert not cmp.right_only, f"unexpected in output under {actual}: {sorted(cmp.right_only)}"
    # filecmp defaults to a shallow (stat-based) comparison; force content comparison.
    _, mismatched, errors = filecmp.cmpfiles(expected, actual, cmp.common_files, shallow=False)
    for name in mismatched:
        # Read both files so pytest renders a helpful unified diff on failure.
        expected_text = (expected / name).read_text(encoding="UTF-8")
        actual_text = (actual / name).read_text(encoding="UTF-8")
        assert actual_text == expected_text, f"content differs for {expected / name}"
    assert not errors, f"could not compare: {errors}"
    for sub in cmp.common_dirs:
        _assert_dircmp(cmp.subdirs[sub], expected / sub, actual / sub)


@pytest.fixture
def assert_trees_equal() -> Callable[[Path, Path], None]:
    """Return a helper that asserts two directory trees are byte-identical."""
    return _assert_trees_equal


@pytest.fixture
def run_kubesplit() -> Callable[..., subprocess.CompletedProcess[bytes]]:
    """Return a helper that runs the real kubesplit CLI in a subprocess.

    Invoking `python -m kubesplit` exercises the true entry point, argument
    parsing, exit code and stdin handling (the reason this tier exists), rather
    than calling the Typer app in-process.
    """

    def _run(args: list[str], stdin: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(
            [sys.executable, "-m", "kubesplit", *args],
            input=stdin,
            capture_output=True,
            check=True,
        )

    return _run
