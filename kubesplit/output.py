"""Some stuff need to get out."""

import os
import shutil

from ruamel.yaml import YAML

default_yaml = YAML(typ="rt")


def create_root_dir(root_directory: str) -> None:
    """create_root_dir."""
    if not os.path.exists(root_directory):
        os.makedirs(root_directory)


def clean_root_dir(root_directory: str) -> None:
    """clean_root_dir."""
    if os.path.isdir(root_directory):
        shutil.rmtree(root_directory)
        os.makedirs(root_directory)


def save_descriptor_to_stream(descriptor, out, yaml_instance=default_yaml):
    """save_descriptor_to_stream."""
    yaml_instance.dump(descriptor.as_yaml, out)


def save_descriptors_to_dir(
    descriptors, root_directory, yaml_instance=default_yaml
):
    """Save input descriptors to files in dir."""
    for _desc_id, desc in descriptors.items():
        with open(
            desc.compute_filename_with_namespace(root_directory), "wt"
        ) as out:
            save_descriptor_to_stream(
                descriptor=desc, out=out, yaml_instance=yaml_instance
            )
