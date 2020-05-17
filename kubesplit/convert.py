"""From input to descriptors."""

import logging
import sys

from ruamel.yaml import YAML
from ruamel.yaml.scanner import ScannerError

from yamkix.config import get_default_yamkix_config, YamkixConfig
from yamkix.yaml_writer import get_opinionated_yaml_writer

from kubesplit.k8s_descriptor import K8SDescriptor
from kubesplit.namespaces import (
    get_all_namespaces,
    prepare_namespace_directories,
)
from kubesplit.output import save_descriptors_to_dir

default_yamkix_config = get_default_yamkix_config()
default_yaml = YAML(typ="rt")


def resource_is_list(resource):
    """Check if the resource is a list."""
    if resource:
        return (
            "kind" in resource
            and "apiVersion" in resource
            and resource["kind"].endswith("List")
        )
    return False


def resource_is_object(resource):
    """Check if the resource is a simple object."""
    if resource:
        return (
            "metadata" in resource
            and "kind" in resource
            and "name" in resource["metadata"]
        )
    return False


def deal_with_list(
    resource, list_index, use_order_prefix, split_lists_to_items: bool = False
):
    """Deal with lists."""
    descriptors = dict()
    if split_lists_to_items:
        print("Not supported yet")
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
    input_ref,
    yaml_reader=default_yaml,
    prefix_resource_files: bool = True,
    split_lists_to_items: bool = False,
):
    """Convert input_ref to a dict of descriptors."""
    parsed = yaml_reader.load_all(input_ref.read())
    descriptors = dict()
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
                        resource_namespace = full_resource["metadata"][
                            "namespace"
                        ]
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
        print(
            "Found [{0}] valid /"
            " [{1}] lists /"
            " [{2}] invalid /"
            " [{3}] empty resources".format(
                nb_valid_resources,
                nb_lists,
                nb_invalid_resources,
                nb_empty_resources,
            )
        )
    except ScannerError as scanner_error:
        print("Something is wrong in the input, got error from Scanner")
        print(scanner_error)
        return dict()
    return descriptors


def convert_input_to_files_in_directory(
    input_name: str,
    root_directory: str,
    prefix_resource_files: bool = True,
    yamkix_config: YamkixConfig = default_yamkix_config,
) -> None:
    """convert_input_to_files_in_directory."""
    yaml = get_opinionated_yaml_writer(yamkix_config)
    if input_name is not None:
        with open(input_name, "rt") as f_input:
            descriptors = convert_input_to_descriptors(
                f_input, yaml, prefix_resource_files=prefix_resource_files
            )
    else:
        descriptors = convert_input_to_descriptors(
            sys.stdin, yaml, prefix_resource_files=prefix_resource_files
        )

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
        logging.error(
            "Nothing found in provided input, check for previous errors"
        )
