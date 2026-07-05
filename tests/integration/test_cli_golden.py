"""End-to-end golden-file tests driving the real kubesplit CLI.

Each scenario runs `kubesplit` against a fixture in ``test-assets/source`` and
diffs the produced output tree against ``test-assets/expected/<fixture>--<config>``.
This is the pytest replacement for the former ``tests.bats`` suite.
"""

import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest

ASSETS_DIR = Path(__file__).parent.parent.parent / "test-assets"
SOURCE_DIR = ASSETS_DIR / "source"
EXPECTED_DIR = ASSETS_DIR / "expected"

pytestmark = pytest.mark.integration

RunKubesplit = Callable[..., subprocess.CompletedProcess[bytes]]
AssertTreesEqual = Callable[[Path, Path], None]


@pytest.mark.parametrize(
    ("fixture", "flags", "config"),
    [
        pytest.param(
            "all-in-one",
            ["--no-quotes-preserved"],
            "no-quotes-preserved",
            id="all-in-one",
        ),
        pytest.param(
            "all-in-one",
            ["--no-quotes-preserved", "--no-resource-prefix"],
            "no-quotes-preserved--no-resource-prefix",
            id="all-in-one-no-resource-prefix",
        ),
        pytest.param(
            "mixed-content-valid-invalid-and-empty-resources",
            ["--no-quotes-preserved"],
            "no-quotes-preserved",
            id="mixed-content-valid-invalid-and-empty",
        ),
        pytest.param(
            "mixed-content-valid-invalid-empty-and-list-resources",
            ["--no-quotes-preserved"],
            "no-quotes-preserved",
            id="mixed-content-valid-invalid-empty-and-list",
        ),
        pytest.param(
            "k8s-deployment-with-comments-1",
            ["--no-quotes-preserved"],
            "no-quotes-preserved",
            id="deployment-with-comments",
        ),
        pytest.param(
            "k8s-deployment-with-comments-1",
            ["--no-quotes-preserved", "--no-resource-prefix", "--spaces-before-comment", "1"],
            "no-quotes-preserved--no-resource-prefix--spaces-before-comment_1",
            id="deployment-with-comments-spaced",
        ),
        pytest.param(
            "formatting-features",
            ["--enforce-block-style"],
            "enforce-block-style",
            id="enforce-block-style",
        ),
        pytest.param(
            "formatting-features",
            ["--align-comments"],
            "align-comments",
            id="align-comments",
        ),
    ],
)
def test_golden_output(
    tmp_path: Path,
    run_kubesplit: RunKubesplit,
    assert_trees_equal: AssertTreesEqual,
    fixture: str,
    flags: list[str],
    config: str,
) -> None:
    """Kubesplit produces the expected output tree for the given fixture and flags."""
    output_dir = tmp_path / "result"
    run_kubesplit(
        [
            "--input",
            str(SOURCE_DIR / f"{fixture}.yml"),
            "--output",
            str(output_dir),
            "--clean-output-dir",
            *flags,
        ]
    )
    assert_trees_equal(EXPECTED_DIR / f"{fixture}--{config}", output_dir)


@pytest.mark.parametrize(
    "input_flag",
    [
        pytest.param([], id="stdin-not-specified"),
        pytest.param(["--input", "-"], id="stdin-is-dash"),
    ],
)
def test_golden_output_from_stdin(
    tmp_path: Path,
    run_kubesplit: RunKubesplit,
    assert_trees_equal: AssertTreesEqual,
    input_flag: list[str],
) -> None:
    """Kubesplit reads STDIN (implicitly or via ``--input -``) and matches the golden tree."""
    output_dir = tmp_path / "result"
    run_kubesplit(
        ["--output", str(output_dir), "--clean-output-dir", "--no-quotes-preserved", *input_flag],
        stdin=(SOURCE_DIR / "all-in-one.yml").read_bytes(),
    )
    assert_trees_equal(EXPECTED_DIR / "all-in-one--no-quotes-preserved", output_dir)


def test_help_exits_zero(run_kubesplit: RunKubesplit) -> None:
    """`kubesplit --help` exits successfully (subprocess helper uses check=True)."""
    result = run_kubesplit(["--help"])
    assert b"Split a set of Kubernetes descriptors" in result.stdout
