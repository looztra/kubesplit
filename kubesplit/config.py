"""Kubesplit configuration helpers."""
import collections
import sys

from argparse import Namespace

import yamkix.config

from kubesplit import __version__

KubesplitConfig = collections.namedtuple(
    "KubesplitConfig",
    "clean_output_dir \
        prefix_resource_files \
        version \
        io_config \
        yamkix_config",
)

KubesplitIOConfig = collections.namedtuple(
    "KubesplitIOConfig", "input input_display_name output_dir",
)


def should_we_show_version(args: Namespace) -> bool:
    """Should we show version or not?."""
    return args.version if args.version is not None else False


def get_io_config_from_args(
    args: Namespace, show_version: bool
) -> KubesplitIOConfig:
    """Build a KubesplitIOConfig from parsed args."""
    input_display_name = "STDIN"
    if args.input is None or args.input == "-":
        f_input = None
    else:
        f_input = args.input
        input_display_name = f_input
    if show_version:
        output_dir = None
    else:
        if args.output_dir is None:
            raise ValueError(
                "the following arguments are required: -o/--output-dir"
            )
        output_dir = args.output_dir
    return KubesplitIOConfig(
        input=f_input,
        input_display_name=input_display_name,
        output_dir=output_dir,
    )


def get_config_from_args(
    args: Namespace, inc_io_config: bool = True
) -> KubesplitConfig:
    """Build a KubesplitConfig from parsed args."""
    show_version: bool = should_we_show_version(args)
    yamkix_config = yamkix.config.get_config_from_args(
        args, inc_io_config=False
    )
    if inc_io_config:
        io_config = get_io_config_from_args(args, show_version)
    else:
        io_config = None
    return KubesplitConfig(
        clean_output_dir=args.clean_output_dir,
        prefix_resource_files=not args.no_resource_prefix,
        version=show_version,
        yamkix_config=yamkix_config,
        io_config=io_config,
    )


def print_config(kubesplit_config: KubesplitConfig):
    """Print a human readable Kubesplit config on stderr."""
    io_config = kubesplit_config.io_config
    print(
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
