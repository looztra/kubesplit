"""Some stuff need to get out."""

import shutil
from pathlib import Path
from typing import TYPE_CHECKING, Any, TextIO, cast

from ruamel.yaml import YAML
from yamkix.comments import align_comments
from yamkix.config import YamkixConfig, get_default_yamkix_config
from yamkix.helpers import convert_flow_to_block_style
from yamkix.yamkix import yamkix_dump_one

from kubesplit.k8s_descriptor import K8SDescriptor

if TYPE_CHECKING:
    from ruamel.yaml.comments import CommentedBase

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
    descriptor: K8SDescriptor,
    out: TextIO,
    yaml_instance: YAML,
    yamkix_config: YamkixConfig = default_yamkix_config,
) -> None:
    """save_descriptor_to_stream."""
    single_item = cast("CommentedBase", descriptor.as_yaml)
    # kubesplit dumps each descriptor through yamkix_dump_one directly (it does not
    # go through yamkix_dump_all), so the block-style and comment-alignment transforms
    # that yamkix_dump_all applies must be replicated here, in the same order.
    if yamkix_config.enforce_block_style:
        convert_flow_to_block_style(data=single_item)
    if yamkix_config.align_comments:
        align_comments(data=single_item)
    yamkix_dump_one(
        single_item,
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
) -> None:
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
