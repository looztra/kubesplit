"""Some stuff need to get out."""

import os
import shutil

from ruamel.yaml import YAML

from yamkix.yamkix import yamkix_dump_one
from yamkix.config import get_default_yamkix_config, YamkixConfig

default_yaml = YAML(typ="rt")
default_yamkix_config = get_default_yamkix_config()


def create_root_dir(root_directory: str) -> None:
    """create_root_dir."""
    if not os.path.exists(root_directory):
        os.makedirs(root_directory)


def clean_root_dir(root_directory: str) -> None:
    """clean_root_dir."""
    if os.path.isdir(root_directory):
        shutil.rmtree(root_directory)
        os.makedirs(root_directory)


def save_descriptor_to_stream(
    descriptor,
    out,
    yaml_instance: YAML,
    yamkix_config: YamkixConfig = default_yamkix_config,
):
    """save_descriptor_to_stream."""
    yamkix_dump_one(
        descriptor.as_yaml,
        yaml_instance,
        yamkix_config.dash_inwards,
        out,
        yamkix_config.spaces_before_comment,
    )


def save_descriptors_to_dir(
    descriptors,
    root_directory,
    yaml_instance: YAML,
    yamkix_config: YamkixConfig = default_yamkix_config,
):
    """Save input descriptors to files in dir."""
    for _desc_id, desc in descriptors.items():
        with open(
            desc.compute_filename_with_namespace(root_directory), "wt"
        ) as out:
            save_descriptor_to_stream(
                descriptor=desc,
                out=out,
                yaml_instance=yaml_instance,
                yamkix_config=yamkix_config,
            )
