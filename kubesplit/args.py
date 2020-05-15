"""Deal with args."""

import argparse


from yamkix.args import add_yamkix_options_to_parser

from kubesplit import __version__
from kubesplit.config import get_config_from_args, KubesplitConfig


def build_parser():
    """Build the cli args parser."""
    parser = argparse.ArgumentParser(
        description="""Kubesplit v{}
            Split a set of Kubernetes descriptors to a set of files.
            The yaml format of the generated files can be tuned using the same\
                parameters as the one used by Yamkix.
            By default, explicit_start is `On`, explicit_end is `Off`\
            and array elements are pushed inwards the start of the \
            matching sequence. Comments are preserved thanks to default \
            parsing mode `rt`.
        """.format(
            __version__
        )
    )
    parser.add_argument(
        "-i",
        "--input",
        required=False,
        help="the file to parse, or STDIN if not specified or if value is -",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        required=False,
        help="the name of the output target directory.\
                The target directory will be created if it does not\
                exist if it's possible",
    )
    parser.add_argument(
        "-c",
        "--clean-output-dir",
        action="store_true",
        help="clean the output directory (rmtree) if set (default is False)",
    )
    parser.add_argument(
        "-p",
        "--no-resource-prefix",
        action="store_true",
        help="by default, resource files are number prefixed, you can disable \
            this behavior with this flag",
    )
    add_yamkix_options_to_parser(
        parser, short_opt_override={"--spaces-before-comment": "-s"}
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="show kubesplit version",
    )
    return parser


def parse_cli(args) -> KubesplitConfig:
    """Parse the cli args."""
    parser = build_parser()
    args = parser.parse_args(args)
    kubesplit_config = get_config_from_args(args, inc_io_config=True)
    return kubesplit_config
