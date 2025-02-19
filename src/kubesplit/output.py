"""Some stuff need to get out."""

import shutil
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML
from yamkix.config import YamkixConfig, get_default_yamkix_config
from yamkix.yamkix import yamkix_dump_one

default_yaml = YAML(typ="rt")
default_yamkix_config = get_default_yamkix_config()


def create_root_dir(root_directory: Path) -> None:
    """create_root_dir."""
    if not root_directory.exists():
        root_directory.mkdir(parents=True)


def clean_root_dir(root_directory: Path) -> None:
    """clean_root_dir."""
    if root_directory.is_dir():
        shutil.rmtree(root_directory)
        root_directory.mkdir(parents=True)


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
    descriptors: dict[str, Any],
    root_directory: Path,
    yaml_instance: YAML,
    yamkix_config: YamkixConfig = default_yamkix_config,
):
    """Save input descriptors to files in dir."""
    for desc in descriptors.values():
        with desc.compute_filename_with_namespace(root_directory).open(
            mode="w",
            encoding="UTF-8",
        ) as out:
            save_descriptor_to_stream(
                descriptor=desc,
                out=out,
                yaml_instance=yaml_instance,
                yamkix_config=yamkix_config,
            )
