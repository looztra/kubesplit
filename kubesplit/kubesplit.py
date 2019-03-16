# -*- coding: utf-8 -*-
"""Main module."""

import sys
import os
import logging
import shutil
import argparse
from ruamel.yaml import YAML
from ruamel.yaml.scanner import ScannerError
from typing import Dict, Set
from .yaml_writer_config import (
    YamlWriterConfig,
    build_yaml_writer_config_from_args,
    get_opinionated_yaml_writer,
)
from .k8s_descriptor import K8SDescriptor


def parse_cli():
    """Parse the cli args"""
    my_args = dict()
    parser = argparse.ArgumentParser(
        description="""Split a set of Kubernetes descriptors to a set of files.
            The yaml format of the generated files can be tuned using the same\
                parameters as the one used by Yamkix.
            By default, explicit_start is `On`, explicit_end is `Off`\
            and array elements are pushed inwards the start of the \
            matching sequence. Comments are preserved thanks to default \
            parsing mode `rt`.
        """
    )
    parser.add_argument(
        "-i",
        "--input",
        required=False,
        help="the file to parse, or STDIN if not specified or if value is -",
    )
    parser.add_argument(
        "-t",
        "--typ",
        required=False,
        default="rt",
        help="the yaml parser mode. Can be `safe` or `rt`",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        required=True,
        help="the name of the output target directory.\
                The target directory will be created if it does not\
                exist if it's possible",
    )
    parser.add_argument(
        "-n",
        "--no-explicit-start",
        action="store_true",
        help="by default, explicit start (---) of the yaml doc \
                is `On`, you can disable it with this option",
    )
    parser.add_argument(
        "-e",
        "--explicit-end",
        action="store_true",
        help="by default, explicit end (...) of the yaml doc \
                is `Off`, you can enable it with this option",
    )
    parser.add_argument(
        "-q",
        "--no-quotes-preserved",
        action="store_true",
        help="by default, quotes are preserved \
                you can disable this with this option",
    )
    parser.add_argument(
        "-f",
        "--default-flow-style",
        action="store_true",
        help="enable the default flow style \
                `Off` by default. In default flow style \
                (with typ=`rt`), maps and lists are written \
                like json",
    )
    parser.add_argument(
        "-d",
        "--no-dash-inwards",
        action="store_true",
        help="by default, dash are pushed inwards \
                use `--no-dash-inwards` to have the dash \
                start at the sequence level",
    )
    parser.add_argument(
        "-c",
        "--clean-output-dir",
        action="store_true",
        help="clean the output directory (rmtree) if set (default is False)",
    )

    args = parser.parse_args()

    input_display_name = "STDIN"
    if args.input is None or args.input == "-":
        my_args["input"] = None
    else:
        my_args["input"] = args.input
        input_display_name = my_args["input"]

    if args.typ not in ["safe", "rt"]:
        raise ValueError(
            "'%s' is not a valid value for option --typ. "
            "Allowed values are 'safe' and 'rt'" % args.type
        )
    my_args["output_dir"] = args.output_dir
    my_args["typ"] = args.typ
    my_args["explicit_start"] = not args.no_explicit_start
    my_args["explicit_end"] = args.explicit_end
    my_args["default_flow_style"] = args.default_flow_style
    my_args["dash_inwards"] = not args.no_dash_inwards
    my_args["quotes_preserved"] = not args.no_quotes_preserved
    my_args["clean_output_dir"] = args.clean_output_dir
    print(
        "Processing: input="
        + input_display_name
        + ", output_dir="
        + my_args["output_dir"]
        + ", clean_output_dir="
        + str(my_args["clean_output_dir"])
        + ", typ="
        + my_args["typ"]
        + ", explicit_start="
        + str(my_args["explicit_start"])
        + ", explicit_end="
        + str(my_args["explicit_end"])
        + ", default_flow_style="
        + str(my_args["default_flow_style"])
        + ", quotes_preserved="
        + str(my_args["quotes_preserved"])
        + ", dash_inwards="
        + str(my_args["dash_inwards"])
    )
    return my_args


def get_all_namespaces(descriptors: Dict[str, K8SDescriptor]) -> Set[str]:
    all_namespaces = set()
    for desc_id, descriptor in descriptors.items():
        if descriptor.hasNamespace():
            all_namespaces.add(descriptor.compute_namespace_dirname())
    return all_namespaces


def prepare_namespace_directories(
    root_directory: str, namespaces: str
) -> None:
    for ns in namespaces:
        ns_dir = os.path.join(root_directory, ns)
        if not os.path.exists(ns_dir):
            logging.info("Creating directory [{0}]".format(ns_dir))
            os.makedirs(ns_dir)


def create_root_dir(root_directory: str) -> None:
    if not os.path.exists(root_directory):
        os.makedirs(root_directory)


def clean_root_dir(root_directory: str) -> None:
    if os.path.isdir(root_directory):
        shutil.rmtree(root_directory)
        os.makedirs(root_directory)


def save_descriptors_to_dir(
    descriptors, root_directory, yaml_instance=YAML(typ="rt")
):
    """save input descriptors to files in dir"""
    for desc_id, desc in descriptors.items():
        with open(
            desc.compute_filename_with_namespace(root_directory), "wt"
        ) as out:
            yaml_instance.dump(desc.as_yaml, out)


def convert_input_to_descriptors(input, yaml_reader=YAML(typ="rt")):
    """convert input (file or STDIN) to a dict of descriptors"""
    if input is not None:
        with open(input, "rt") as f_input:
            parsed = yaml_reader.load_all(f_input.read())
    else:
        parsed = yaml_reader.load_all(sys.stdin.read())
    descriptors = dict()
    try:
        # Read the parsed content to force the scanner to issue errors if any
        for full_resource in parsed:
            resource_name = full_resource["metadata"]["name"]
            resource_kind = full_resource["kind"]
            if "namespace" in full_resource["metadata"]:
                resource_namespace = full_resource["metadata"]["namespace"]
            else:
                resource_namespace = None
            k8s_descriptor = K8SDescriptor(
                resource_name, resource_kind, resource_namespace, full_resource
            )
            descriptors[k8s_descriptor.id] = k8s_descriptor
    except ScannerError as e:
        print("Something is wrong in the input, got error from Scanner")
        print(e)
        return dict()
    return descriptors


def convert_input_to_files_in_directory(
    input_name: str,
    root_directory: str,
    writer_config: YamlWriterConfig = YamlWriterConfig(),
) -> None:
    yaml = get_opinionated_yaml_writer(writer_config)
    descriptors = convert_input_to_descriptors(input_name, yaml)
    if len(descriptors) > 0:
        namespaces = get_all_namespaces(descriptors)
        prepare_namespace_directories(root_directory, namespaces)
        save_descriptors_to_dir(descriptors, root_directory, yaml)
    else:
        logging.error(
            "Nothing found in provided input, check for previous errors"
        )


def split_input_to_files(
    root_directory: str,
    input_name: str,
    clean_output_dir: bool = True,
    writer_config: YamlWriterConfig = YamlWriterConfig(),
) -> None:
    """
    split input to files

    Args:
        root_directory: the directory where files and namespace directories\
            will be created
        input_name: the name of the input file to read. If None, then STDIN\
            will be used
        clean_output_dir: do we cleanup the target directory before processing?
        writer_config: YamlWriterConfig object describing how to format the\
            yaml files that will be written
    """
    create_root_dir(root_directory)
    if clean_output_dir:
        clean_root_dir(root_directory)
    convert_input_to_files_in_directory(
        input_name=input_name,
        root_directory=root_directory,
        writer_config=writer_config,
    )


def main():
    """
    Parse args and call the split mojo
    """

    parsed_args = parse_cli()
    root_directory = parsed_args["output_dir"]
    clean_output_dir = parsed_args["clean_output_dir"]
    input_name = parsed_args["input"]
    split_input_to_files(
        root_directory=root_directory,
        input_name=input_name,
        clean_output_dir=clean_output_dir,
        writer_config=build_yaml_writer_config_from_args(parsed_args),
    )


if __name__ == "__main__":
    main()
