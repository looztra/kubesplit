"""Kubesplit configuration helpers."""

import sys
from dataclasses import dataclass

from yamkix import get_yamkix_config_from_default
from yamkix.config import YamkixConfig

from kubesplit import __version__
from kubesplit.errors import MissingOutputDirError


@dataclass
class KubesplitIOConfig:
    """Represents Kubesplit input/output configuration."""

    input: str | None
    input_display_name: str
    output_dir: str


@dataclass
class KubesplitConfig:
    """Represents Kubesplit configuration."""

    clean_output_dir: bool
    prefix_resource_files: bool
    version: bool
    io_config: KubesplitIOConfig
    yamkix_config: YamkixConfig


def get_io_config_from_typer_args(
    input_file: str | None,
    output_dir: str | None,
    show_version: bool,
) -> KubesplitIOConfig:
    """Build a KubesplitIOConfig from typed CLI args."""
    if input_file is None or input_file == "-":
        f_input = None
        input_display_name = "STDIN"
    else:
        f_input = input_file
        input_display_name = f_input
    if show_version:
        resolved_output_dir = "N/A"
    else:
        if output_dir is None:
            raise MissingOutputDirError
        resolved_output_dir = output_dir
    return KubesplitIOConfig(
        input=f_input,
        input_display_name=input_display_name,
        output_dir=resolved_output_dir,
    )


def get_kubesplit_config_from_typer_args(  # noqa: PLR0913
    input_file: str | None,
    output_dir: str | None,
    clean_output_dir: bool,
    no_resource_prefix: bool,
    show_version: bool,
    typ: str,
    no_explicit_start: bool,
    explicit_end: bool,
    no_quotes_preserved: bool,
    enforce_double_quotes: bool,
    default_flow_style: bool,
    no_dash_inwards: bool,
    spaces_before_comment: int | None,
    line_width: int,
) -> KubesplitConfig:
    """Build a KubesplitConfig from typed Typer CLI arguments."""
    io_config = get_io_config_from_typer_args(input_file, output_dir, show_version)
    yamkix_config = get_yamkix_config_from_default(
        parsing_mode=typ,
        explicit_start=not no_explicit_start,
        explicit_end=explicit_end,
        default_flow_style=default_flow_style,
        dash_inwards=not no_dash_inwards,
        quotes_preserved=not no_quotes_preserved,
        enforce_double_quotes=enforce_double_quotes,
        spaces_before_comment=spaces_before_comment,
        line_width=line_width,
    )
    return KubesplitConfig(
        clean_output_dir=clean_output_dir,
        prefix_resource_files=not no_resource_prefix,
        version=show_version,
        yamkix_config=yamkix_config,
        io_config=io_config,
    )


def print_config(kubesplit_config: KubesplitConfig) -> None:
    """Print a human readable Kubesplit config on stderr."""
    io_config = kubesplit_config.io_config
    if io_config.output_dir is None:
        raise SystemExit
    print(  # noqa: T201
        "[kubesplit("
        + __version__
        + ")] Processing: input="
        + io_config.input_display_name
        + ", output_dir="
        + io_config.output_dir
        + ", clean_output_dir="
        + str(kubesplit_config.clean_output_dir)
        + ", prefix_resource_files="
        + str(kubesplit_config.prefix_resource_files)
        + ", typ="
        + kubesplit_config.yamkix_config.parsing_mode
        + ", explicit_start="
        + str(kubesplit_config.yamkix_config.explicit_start)
        + ", explicit_end="
        + str(kubesplit_config.yamkix_config.explicit_end)
        + ", default_flow_style="
        + str(kubesplit_config.yamkix_config.default_flow_style)
        + ", quotes_preserved="
        + str(kubesplit_config.yamkix_config.quotes_preserved)
        + ", dash_inwards="
        + str(kubesplit_config.yamkix_config.dash_inwards)
        + ", spaces_before_comment="
        + str(kubesplit_config.yamkix_config.spaces_before_comment)
        + ", show_version="
        + str(kubesplit_config.version),
        file=sys.stderr,
    )
