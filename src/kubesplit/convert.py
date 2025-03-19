"""From input to descriptors."""

import logging
import sys
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.scanner import ScannerError
from yamkix.config import YamkixConfig, get_default_yamkix_config
from yamkix.yaml_writer import get_opinionated_yaml_writer

from kubesplit.k8s_descriptor import K8SDescriptor
from kubesplit.namespaces import get_all_namespaces, prepare_namespace_directories
from kubesplit.output import save_descriptors_to_dir

LOGGER = logging.getLogger(__name__)
default_yamkix_config = get_default_yamkix_config()
default_yaml = YAML(typ="rt")
StreamTextType = Any


def resource_is_list(resource: dict[str, Any]) -> bool:
    """Check if the resource is a list."""
    if resource:
        return "kind" in resource and "apiVersion" in resource and resource["kind"].endswith("List")
    return False


def resource_is_object(resource: dict[str, Any]) -> bool:
    """Check if the resource is a simple object."""
    if resource:
        return "metadata" in resource and "kind" in resource and "name" in resource["metadata"]
    return False


def deal_with_list(
    resource: dict[str, Any], list_index: int, use_order_prefix: bool, split_lists_to_items: bool = False
) -> dict[str, Any]:
    """Deal with lists."""
    descriptors = {}
    if split_lists_to_items:
        print("Not supported yet")  # noqa: T201
    else:
        list_name = "list_" + str(list_index)
        k8s_descriptor = K8SDescriptor(
            name=list_name,
            kind=resource["kind"],
            namespace=None,
            as_yaml=resource,
            use_order_prefix=use_order_prefix,
        )
        descriptors[k8s_descriptor.id] = k8s_descriptor
    return descriptors


# pylint: disable=too-many-locals
def convert_input_to_descriptors(
    input_ref: StreamTextType,
    yaml_reader: YAML = default_yaml,
    prefix_resource_files: bool = True,
    split_lists_to_items: bool = False,
) -> dict[str, Any]:
    """Convert input_ref to a dict of descriptors."""
    parsed = yaml_reader.load_all(input_ref.read())
    descriptors = {}
    try:
        nb_empty_resources = 0
        nb_invalid_resources = 0
        nb_valid_resources = 0
        nb_lists = 0
        # Read the parsed content to force the scanner to issue errors if any
        for full_resource in parsed:
            if full_resource:
                if resource_is_object(full_resource):
                    resource_name = full_resource["metadata"]["name"]
                    resource_kind = full_resource["kind"]
                    if "namespace" in full_resource["metadata"]:
                        resource_namespace = full_resource["metadata"]["namespace"]
                    else:
                        resource_namespace = None
                    k8s_descriptor = K8SDescriptor(
                        name=resource_name,
                        kind=resource_kind,
                        namespace=resource_namespace,
                        as_yaml=full_resource,
                        use_order_prefix=prefix_resource_files,
                    )
                    descriptors[k8s_descriptor.id] = k8s_descriptor
                    nb_valid_resources = nb_valid_resources + 1
                elif resource_is_list(full_resource):
                    descriptors_from_list = deal_with_list(
                        full_resource,
                        nb_lists,
                        prefix_resource_files,
                        split_lists_to_items=split_lists_to_items,
                    )
                    descriptors.update(descriptors_from_list)
                    nb_lists = nb_lists + 1
                else:
                    nb_invalid_resources = nb_invalid_resources + 1
            else:
                nb_empty_resources = nb_empty_resources + 1
        print(  # noqa: T201
            f"Found [{nb_valid_resources}] valid /"
            f" [{nb_lists}] lists /"
            f" [{nb_invalid_resources}] invalid /"
            f" [{nb_empty_resources}] empty resources"
        )
    except ScannerError as scanner_error:
        print("Something is wrong in the input, got error from Scanner")  # noqa: T201
        print(scanner_error)  # noqa: T201
        return {}
    return descriptors


def convert_input_to_files_in_directory(
    input_name: Path | None,
    root_directory: Path,
    prefix_resource_files: bool = True,
    yamkix_config: YamkixConfig = default_yamkix_config,
) -> None:
    """convert_input_to_files_in_directory."""
    yaml = get_opinionated_yaml_writer(yamkix_config)
    if input_name is not None:
        with input_name.open(encoding="UTF-8") as f_input:
            descriptors = convert_input_to_descriptors(f_input, yaml, prefix_resource_files=prefix_resource_files)
    else:
        descriptors = convert_input_to_descriptors(sys.stdin, yaml, prefix_resource_files=prefix_resource_files)

    if len(descriptors) > 0:
        namespaces = get_all_namespaces(descriptors)
        prepare_namespace_directories(root_directory, namespaces)
        save_descriptors_to_dir(
            descriptors,
            root_directory,
            yaml_instance=yaml,
            yamkix_config=yamkix_config,
        )
    else:
        LOGGER.error("Nothing found in provided input, check for previous errors")
