# -*- coding: utf-8 -*-
"""Main module."""
import sys
import os
import logging
import shutil
import argparse
from ruamel.yaml import YAML
from typing import Dict, Set


class YamlWriterConfig:
    """
    Config stanza for ruamel.yaml.YAML parser/writer with opinionated defaults
    """

    def __init__(self, explicit_start: bool = True,
                 explicit_end: bool = False,
                 default_flow_style: bool = False,
                 dash_inwards: bool = True,
                 quotes_preserved: bool = True,
                 parsing_mode: str = 'rt'):
        """
            Args:

            explicit_start: write the start of the yaml doc even when there is \
                only one done in the file
            default_flow_style: if False, block style will be used for nested \
                    arrays/maps
            dash_inwards: push dash inwards if True
            quotes_preserved: preserve quotes if True
            parsing_typ: safe or roundtrip (rt)
        """
        self.explicit_start = explicit_start
        self.explicit_end = explicit_end
        self.default_flow_style = default_flow_style
        self.dash_inwards = dash_inwards
        self.quotes_preserved = quotes_preserved
        self.parsing_mode = parsing_mode


class K8SDescriptor:
    """Kubernetes descriptor"""

    _cluster_wide_str_rep = "__clusterwide__"
    _order_prefixes = {
        "namespace": "00",
        "serviceaccount": "01",
        "clusterrole": "02",
        "role": "03",
        "clusterrolebinding": "04",
        "rolebinding": "05",
    }

    def __init__(self, name: str, kind: str, namespace: str, as_yaml):
        self.name = name
        self.kind = kind
        self.namespace = namespace
        self.as_yaml = as_yaml
        if namespace is None:
            ns_or_cluster_wide = K8SDescriptor._cluster_wide_str_rep
        else:
            ns_or_cluster_wide = namespace
        self.id = "ns:{0}/kind:{1}/name:{2}".format(
            ns_or_cluster_wide, kind, name)

    def hasNamespace(self) -> bool:
        return self.namespace is not None

    def compute_namespace_dirname(self) -> str:
        if self.hasNamespace():
            return self.namespace.lower()
        else:
            return None

    def compute_filename(self) -> str:
        return "{0}{1}--{2}.yml".format(
            self.get_order_prefix(),
            self.kind.lower(),
            self.name.lower().replace(":", "-")
        )

    def get_order_prefix(self) -> str:
        if self.kind.lower() in K8SDescriptor._order_prefixes:
            return "{0}--".format(K8SDescriptor._order_prefixes[self.kind.lower()])
        else:
            return ''

    def compute_filename_with_namespace(self, root_directory) -> str:
        if(self.hasNamespace()):
            return os.path.join(root_directory, self.compute_namespace_dirname(), self.compute_filename())
        else:
            return os.path.join(root_directory, self.compute_filename())


def parse_cli():
    """Parse the cli args"""
    my_args = dict()
    parser = argparse.ArgumentParser(
        description='''Split a set of Kubernetes descriptors to a set of files.
            The yaml format of the generated files can be tuned using the same \
                parameters as the one used by Yamkix.
            By default, explicit_start is `On`, explicit_end is `Off`\
            and array elements are pushed inwards the start of the \
            matching sequence. Comments are preserved thanks to default \
            parsing mode `rt`.
        ''')
    parser.add_argument('-i',
                        '--input',
                        required=False,
                        help='the file to parse, or STDIN if not specified or if value is -')
    parser.add_argument('-t',
                        '--typ',
                        required=False,
                        default='rt',
                        help='the yaml parser mode. Can be `safe` or `rt`')
    parser.add_argument('-o', '--output-dir',
                        required=True,
                        help='the name of the output target directory.\
                            The target directory will be created if it does not exist \
                                if it\'s possible')
    parser.add_argument('-n', '--no-explicit-start',
                        action='store_true',
                        help='by default, explicit start (---) of the yaml doc \
                                is `On`, you can disable it with this option')
    parser.add_argument('-e', '--explicit-end',
                        action='store_true',
                        help='by default, explicit end (...) of the yaml doc \
                                is `Off`, you can enable it with this option')
    parser.add_argument('-q', '--no-quotes-preserved',
                        action='store_true',
                        help='by default, quotes are preserved \
                                you can disable this with this option')
    parser.add_argument('-f', '--default-flow-style',
                        action='store_true',
                        help='enable the default flow style \
                                `Off` by default. In default flow style \
                                (with typ=`rt`), maps and lists are written \
                                like json')
    parser.add_argument('-d', '--no-dash-inwards',
                        action='store_true',
                        help='by default, dash are pushed inwards \
                                use `--no-dash-inwards` to have the dash \
                                start at the sequence level')
    parser.add_argument('-c', '--clean-output-dir',
                        action='store_true',
                        help='clean the output directory (rmtree) if set (default is False)')

    args = parser.parse_args()

    input_display_name = "STDIN"
    if args.input is None or args.input == '-':
        my_args['input'] = None
    else:
        my_args['input'] = args.input
        input_display_name = my_args['input']

    if args.typ not in ["safe", "rt"]:
        raise ValueError(
            "'%s' is not a valid value for option --typ. "
            "Allowed values are 'safe' and 'rt'" % args.type)
    my_args['output_dir'] = args.output_dir
    my_args['typ'] = args.typ
    my_args['explicit_start'] = not args.no_explicit_start
    my_args['explicit_end'] = args.explicit_end
    my_args['default_flow_style'] = args.default_flow_style
    my_args['dash_inwards'] = not args.no_dash_inwards
    my_args['quotes_preserved'] = not args.no_quotes_preserved
    my_args['clean_output_dir'] = args.clean_output_dir
    print("Processing: input=" + input_display_name +
          ", output_dir=" + my_args['output_dir'] +
          ", clean_output_dir=" + str(my_args['clean_output_dir']) +
          ", typ=" + my_args['typ'] +
          ", explicit_start=" + str(my_args['explicit_start']) +
          ", explicit_end=" + str(my_args['explicit_end']) +
          ", default_flow_style=" + str(my_args['default_flow_style']) +
          ", quotes_preserved=" + str(my_args['quotes_preserved']) +
          ", dash_inwards=" + str(my_args['dash_inwards']))
    return my_args


def get_all_namespace(descriptors: Dict[str, K8SDescriptor]) -> Set[str]:
    all_namespaces = set()
    for desc_id, descriptor in descriptors.items():
        if descriptor.hasNamespace():
            all_namespaces.add(descriptor.compute_namespace_dirname())
    return all_namespaces


def prepare_namespace_directories(root_directory: str, namespaces: str) -> None:
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


def save_descriptors_to_dir(descriptors, root_directory, yaml_instance=YAML(typ="rt")):
    """save input descriptors to files in dir"""
    for desc_id, desc in descriptors.items():
        with open(desc.compute_filename_with_namespace(root_directory), "wt") as out:
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


def get_opinionated_yaml_writer(writer_config: YamlWriterConfig = YamlWriterConfig()) -> YAML:
    """
    Configure a yaml parser/formatter the yamkix way

    Args:

        writer_config: a YamlWriterConfig instance

    Returns:

        a ruamel.yaml object
    """
    yaml = YAML(typ=writer_config.parsing_mode)
    yaml.explicit_start = writer_config.explicit_start
    yaml.explicit_end = writer_config.explicit_end
    yaml.default_flow_style = writer_config.default_flow_style
    yaml.preserve_quotes = writer_config.quotes_preserved
    if writer_config.dash_inwards:
        yaml.indent(mapping=2, sequence=4, offset=2)
    return yaml


def convert_input_to_files_in_directory(input, root_directory: str) -> None:
    yaml = get_opinionated_yaml_writer()
    descriptors = convert_input_to_descriptors(input, yaml)
    if len(descriptors) > 0:
        namespaces = get_all_namespace(descriptors)
        prepare_namespace_directories(root_directory, namespaces)
        save_descriptors_to_dir(descriptors, root_directory, yaml)
    else:
        logging.error(
            "Nothing found in provided input, check for previous errors")


def main():
    """
    split input to files
    """

    parsed_args = parse_cli()
    root_directory = parsed_args['output_dir']
    create_root_dir(root_directory)
    if parsed_args['clean_output_dir']:
        clean_root_dir(root_directory)
    convert_input_to_files_in_directory(
        input=parsed_args['input'], root_directory=root_directory)


if __name__ == "__main__":
    main()
