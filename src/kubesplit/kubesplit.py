"""Main module."""

import sys
from pathlib import Path

from kubesplit.args import parse_cli
from kubesplit.config import KubesplitConfig, print_config
from kubesplit.convert import convert_input_to_files_in_directory
from kubesplit.helpers import print_version
from kubesplit.output import clean_root_dir, create_root_dir


def split_input_to_files(kubesplit_config: KubesplitConfig) -> None:
    """Split input to files."""
    root_directory = Path(kubesplit_config.io_config.output_dir)
    clean_output_dir = kubesplit_config.clean_output_dir
    prefix_resource_files = kubesplit_config.prefix_resource_files
    input_name = kubesplit_config.io_config.input
    yamkix_config = kubesplit_config.yamkix_config

    create_root_dir(root_directory)
    if clean_output_dir:
        clean_root_dir(root_directory)
    convert_input_to_files_in_directory(
        input_name=Path(input_name) if input_name is not None else None,
        root_directory=root_directory,
        prefix_resource_files=prefix_resource_files,
        yamkix_config=yamkix_config,
    )


def main() -> None:
    """Parse args and call the split mojo."""
    kubesplit_config = parse_cli(sys.argv[1:])
    if kubesplit_config.version:
        print_version()
    else:
        print_config(kubesplit_config)
        split_input_to_files(kubesplit_config)


if __name__ == "__main__":
    main()
