"""Tests for the typer-based CLI (kubesplit._cli)."""

from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from kubesplit._cli import app
from kubesplit.helpers import get_version_string

runner = CliRunner()


def test_version_flag() -> None:
    """--version / -v prints version string and exits with 0."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert get_version_string() in result.output


def test_version_short_flag() -> None:
    """-v is an alias for --version."""
    result = runner.invoke(app, ["-v"])
    assert result.exit_code == 0
    assert get_version_string() in result.output


def test_missing_output_dir_exits_nonzero() -> None:
    """Invoking without -o/--output-dir should fail with a non-zero exit."""
    result = runner.invoke(app, [])
    assert result.exit_code != 0


@pytest.mark.parametrize(
    "extra_args",
    [
        pytest.param([], id="defaults"),
        pytest.param(["-c"], id="clean-output-dir"),
        pytest.param(["-p"], id="no-resource-prefix"),
        pytest.param(["-n"], id="no-explicit-start"),
        pytest.param(["-e"], id="explicit-end"),
        pytest.param(["-q"], id="no-quotes-preserved"),
        pytest.param(["-f"], id="default-flow-style"),
        pytest.param(["-d"], id="no-dash-inwards"),
        pytest.param(["-s", "2"], id="spaces-before-comment"),
        pytest.param(["-t", "safe"], id="typ-safe"),
        pytest.param(["-w", "120"], id="line-width"),
        pytest.param(["-E"], id="enforce-double-quotes"),
    ],
)
def test_all_flags_accepted(tmp_path: Path, extra_args: list[str]) -> None:
    """All documented CLI flags are accepted without error."""
    input_yaml = tmp_path / "input.yaml"
    input_yaml.write_text("---\napiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: foo\n  namespace: bar\ndata: {}\n")
    output_dir = tmp_path / "out"
    with patch("kubesplit._cli.split_input_to_files"):
        result = runner.invoke(app, ["-i", str(input_yaml), "-o", str(output_dir), *extra_args])
    assert result.exit_code == 0, result.output


def test_stdin_is_used_when_no_input_flag(tmp_path: Path) -> None:
    """-i flag is optional; omitting it uses STDIN (display name shows STDIN)."""
    output_dir = tmp_path / "out"
    with patch("kubesplit._cli.split_input_to_files") as mock_split:
        result = runner.invoke(app, ["-o", str(output_dir)])
    assert result.exit_code == 0, result.output
    config = mock_split.call_args[0][0]
    assert config.io_config.input is None
    assert config.io_config.input_display_name == "STDIN"


def test_input_dash_treated_as_stdin(tmp_path: Path) -> None:
    """-i - is equivalent to reading from STDIN."""
    output_dir = tmp_path / "out"
    with patch("kubesplit._cli.split_input_to_files") as mock_split:
        result = runner.invoke(app, ["-i", "-", "-o", str(output_dir)])
    assert result.exit_code == 0, result.output
    config = mock_split.call_args[0][0]
    assert config.io_config.input is None


def test_clean_output_dir_flag_sets_config(tmp_path: Path) -> None:
    """-c/--clean-output-dir sets clean_output_dir=True in config."""
    output_dir = tmp_path / "out"
    with patch("kubesplit._cli.split_input_to_files") as mock_split:
        runner.invoke(app, ["-o", str(output_dir), "-c"])
    config = mock_split.call_args[0][0]
    assert config.clean_output_dir is True


def test_no_resource_prefix_flag_sets_config(tmp_path: Path) -> None:
    """-p/--no-resource-prefix disables the order prefix in config."""
    output_dir = tmp_path / "out"
    with patch("kubesplit._cli.split_input_to_files") as mock_split:
        runner.invoke(app, ["-o", str(output_dir), "-p"])
    config = mock_split.call_args[0][0]
    assert config.prefix_resource_files is False


def test_typ_safe_sets_parsing_mode(tmp_path: Path) -> None:
    """-t safe sets parsing_mode='safe' in the yamkix config."""
    output_dir = tmp_path / "out"
    with patch("kubesplit._cli.split_input_to_files") as mock_split:
        runner.invoke(app, ["-o", str(output_dir), "-t", "safe"])
    config = mock_split.call_args[0][0]
    assert config.yamkix_config.parsing_mode == "safe"


def test_spaces_before_comment_short_flag(tmp_path: Path) -> None:
    """-s N sets spaces_before_comment=N (kubesplit uses -s, not yamkix's -c)."""
    expected_spaces = 4
    output_dir = tmp_path / "out"
    with patch("kubesplit._cli.split_input_to_files") as mock_split:
        runner.invoke(app, ["-o", str(output_dir), "-s", str(expected_spaces)])
    config = mock_split.call_args[0][0]
    assert config.yamkix_config.spaces_before_comment == expected_spaces
