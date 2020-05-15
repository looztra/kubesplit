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


def convert_input_to_descriptors(
    input_ref, yaml_reader=default_yaml, prefix_resource_files: bool = True
):
    """Convert input_ref to a dict of descriptors."""
    parsed = yaml_reader.load_all(input_ref.read())
    descriptors = dict()
    try:
        nb_empty_resources = 0
        nb_invalid_resources = 0
        nb_valid_resources = 0
        # Read the parsed content to force the scanner to issue errors if any
        for full_resource in parsed:
            if full_resource:
                if (
                    "metadata" in full_resource
                    and "kind" in full_resource
                    and "name" in full_resource["metadata"]
                ):
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
                else:
                    nb_invalid_resources = nb_invalid_resources + 1
            else:
                nb_empty_resources = nb_empty_resources + 1
        print(
            "Found [{0}] valid / [{1}] invalid / [{2}] empty resources".format(
                nb_valid_resources, nb_invalid_resources, nb_empty_resources
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
        save_descriptors_to_dir(descriptors, root_directory, yaml)
    else:
        logging.error(
            "Nothing found in provided input, check for previous errors"
        )
