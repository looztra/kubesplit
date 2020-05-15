"""Main module."""

import sys
import os
import logging
import shutil
from typing import Dict, Set

from ruamel.yaml import YAML
from ruamel.yaml.scanner import ScannerError

from yamkix.config import get_default_yamkix_config, YamkixConfig
from yamkix.yaml_writer import get_opinionated_yaml_writer

from kubesplit.args import parse_cli
from kubesplit.config import KubesplitConfig, print_config
from kubesplit.helpers import print_version
from kubesplit.k8s_descriptor import K8SDescriptor

default_yaml = YAML(typ="rt")
default_yamkix_config = get_default_yamkix_config()


def get_all_namespaces(descriptors: Dict[str, K8SDescriptor]) -> Set[str]:
    """get_all_namespaces."""
    all_namespaces = set()
    for _desc_id, descriptor in descriptors.items():
        if descriptor.has_namespace():
            all_namespaces.add(descriptor.compute_namespace_dirname())
    return all_namespaces


def prepare_namespace_directories(
    root_directory: str, namespaces: str
) -> None:
    """prepare_namespace_directories."""
    for namespace in namespaces:
        ns_dir = os.path.join(root_directory, namespace)
        if not os.path.exists(ns_dir):
            logging.info("Creating directory [%s]", ns_dir)
            os.makedirs(ns_dir)


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


def split_input_to_files(kubesplit_config: KubesplitConfig) -> None:
    """Split input to files.

    Args:
        root_directory: the directory where files and namespace directories\
            will be created
        input_name: the name of the input file to read. If None, then STDIN\
            will be used
        clean_output_dir: do we cleanup the target directory before processing?
        yamkix_config: YamkixConfig object describing how to format the\
            yaml files that will be written
    """
    root_directory = kubesplit_config.io_config.output_dir
    clean_output_dir = kubesplit_config.clean_output_dir
    prefix_resource_files = kubesplit_config.prefix_resource_files
    input_name = kubesplit_config.io_config.input
    yamkix_config = kubesplit_config.yamkix_config

    create_root_dir(root_directory)
    if clean_output_dir:
        clean_root_dir(root_directory)
    convert_input_to_files_in_directory(
        input_name=input_name,
        root_directory=root_directory,
        prefix_resource_files=prefix_resource_files,
        yamkix_config=yamkix_config,
    )


def main():
    """Parse args and call the split mojo."""
    kubesplit_config = parse_cli(sys.argv[1:])
    if kubesplit_config.version:
        print_version()
    else:
        print_config(kubesplit_config)
        split_input_to_files(kubesplit_config)


if __name__ == "__main__":
    main()
