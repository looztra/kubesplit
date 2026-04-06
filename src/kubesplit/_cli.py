"""Typer-based CLI implementation for kubesplit."""

from enum import Enum
from typing import Annotated

import typer
from yamkix.config import DEFAULT_LINE_WIDTH

from kubesplit import __version__
from kubesplit.config import KubesplitConfig, get_kubesplit_config_from_typer_args, print_config
from kubesplit.helpers import get_version_string
from kubesplit.kubesplit import split_input_to_files

app = typer.Typer(
    name="kubesplit",
    help=f"Kubesplit v{__version__}. Split a set of Kubernetes descriptors to a set of files.",
    context_settings={"help_option_names": ["-h", "--help"]},
    add_completion=False,
    no_args_is_help=False,
)


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        typer.echo(get_version_string())
        raise typer.Exit(code=0)


# We cannot use StrEnum as we want to support python 3.10 too
class SupportedYamlParserMode(str, Enum):
    """Supported YAML parser modes."""

    SAFE = "safe"
    RT = "rt"


@app.command()
def main(  # noqa: PLR0913
    input_file: Annotated[
        str | None,
        typer.Option(
            "-i",
            "--input",
            help="the file to parse, or STDIN if not specified or if value is -",
        ),
    ] = None,
    output_dir: Annotated[
        str | None,
        typer.Option(
            "-o",
            "--output-dir",
            "--output",
            help="the name of the output target directory. The target directory will be created if it does not exist.",
        ),
    ] = None,
    clean_output_dir: Annotated[
        bool,
        typer.Option(
            "-c",
            "--clean-output-dir",
            help="clean the output directory (rmtree) if set (default is False)",
        ),
    ] = False,
    no_resource_prefix: Annotated[
        bool,
        typer.Option(
            "-p",
            "--no-resource-prefix",
            help="by default, resource files are number prefixed, you can disable this behavior with this flag",
        ),
    ] = False,
    typ: Annotated[
        SupportedYamlParserMode,
        typer.Option(
            "-t",
            "--typ",
            help="the yaml parser mode. Can be 'safe' or 'rt'. Using 'safe' will remove all comments.",
            case_sensitive=False,
        ),
    ] = SupportedYamlParserMode.RT,
    no_explicit_start: Annotated[
        bool,
        typer.Option(
            "-n",
            "--no-explicit-start",
            help="by default, explicit start of the yaml doc is 'On', you can disable it with this option.",
        ),
    ] = False,
    explicit_end: Annotated[
        bool,
        typer.Option(
            "-e",
            "--explicit-end",
            help="by default, explicit end of the yaml doc is 'Off', you can enable it with this option.",
        ),
    ] = False,
    no_quotes_preserved: Annotated[
        bool,
        typer.Option(
            "-q",
            "--no-quotes-preserved",
            help="by default, quotes are preserved, you can disable this with this option.",
        ),
    ] = False,
    enforce_double_quotes: Annotated[
        bool,
        typer.Option(
            "-E",
            "--enforce-double-quotes",
            help="enforce double quotes when --no-quotes-preserved is activated",
        ),
    ] = False,
    default_flow_style: Annotated[
        bool,
        typer.Option(
            "-f",
            "--default-flow-style",
            help="enable the default flow style (Off by default).",
        ),
    ] = False,
    no_dash_inwards: Annotated[
        bool,
        typer.Option(
            "-d",
            "--no-dash-inwards",
            help="by default, dashes are pushed inwards. Use '--no-dash-inwards' to disable.",
        ),
    ] = False,
    spaces_before_comment: Annotated[
        int | None,
        typer.Option(
            "-s",
            "--spaces-before-comment",
            help="specify the number of spaces between comments and content."
            " If not specified, comments are left as is.",
        ),
    ] = None,
    line_width: Annotated[
        int,
        typer.Option(
            "-w",
            "--line-width",
            help="specify the maximum line width.",
        ),
    ] = DEFAULT_LINE_WIDTH,
    _version: Annotated[
        bool,
        typer.Option("-v", "--version", help="show kubesplit version", callback=version_callback),
    ] = False,
) -> None:
    """Split a set of Kubernetes descriptors to a set of files.

    The yaml format of the generated files can be tuned using the same
    parameters as yamkix. By default, explicit_start is 'On', explicit_end
    is 'Off' and array elements are pushed inwards. Comments are preserved
    thanks to default parsing mode 'rt'.
    """
    kubesplit_config: KubesplitConfig = get_kubesplit_config_from_typer_args(
        input_file=input_file,
        output_dir=output_dir,
        clean_output_dir=clean_output_dir,
        no_resource_prefix=no_resource_prefix,
        show_version=False,
        typ=typ.value,
        no_explicit_start=no_explicit_start,
        explicit_end=explicit_end,
        no_quotes_preserved=no_quotes_preserved,
        enforce_double_quotes=enforce_double_quotes,
        default_flow_style=default_flow_style,
        no_dash_inwards=no_dash_inwards,
        spaces_before_comment=spaces_before_comment,
        line_width=line_width,
    )
    print_config(kubesplit_config)
    split_input_to_files(kubesplit_config)


if __name__ == "__main__":
    app()  # pragma: no cover
