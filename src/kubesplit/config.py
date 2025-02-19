"""Kubesplit configuration helpers."""

import sys
from argparse import Namespace
from dataclasses import dataclass

from yamkix.config import YamkixConfig
from yamkix.config import get_config_from_args as yamkix_get_config_from_args

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


def should_we_show_version(args: Namespace) -> bool:
    """Should we show version or not?."""
    return args.version if args.version is not None else False


def get_io_config_from_args(args: Namespace, show_version: bool) -> KubesplitIOConfig:
    """Build a KubesplitIOConfig from parsed args."""
    input_display_name = "STDIN"
    if args.input is None or args.input == "-":
        f_input = None
    else:
        f_input = args.input
        input_display_name = f_input
    if show_version:
        output_dir = "N/A"
    else:
        if args.output_dir is None:
            raise MissingOutputDirError
        output_dir = args.output_dir
    return KubesplitIOConfig(
        input=f_input,
        input_display_name=input_display_name,
        output_dir=output_dir,
    )


def get_config_from_args(args: Namespace) -> KubesplitConfig:
    """Build a KubesplitConfig from parsed args."""
    show_version: bool = should_we_show_version(args)
    yamkix_config = yamkix_get_config_from_args(args, inc_io_config=False)
    io_config = get_io_config_from_args(args, show_version)
    return KubesplitConfig(
        clean_output_dir=args.clean_output_dir,
        prefix_resource_files=not args.no_resource_prefix,
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
