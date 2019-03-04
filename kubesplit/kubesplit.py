# -*- coding: utf-8 -*-
import sys
import os
from ruamel.yaml import YAML

"""Main module."""


class K8SDescriptor:
    """Kubernetes descriptor"""

    def __init__(self, name, kind, namespace, as_yaml):
        self.name = name
        self.kind = kind
        self.namespace = namespace
        self.as_yaml = as_yaml
        if namespace is None:
            ns_or_cluster_wide = "clusterwide"
        else:
            ns_or_cluster_wide = namespace
        self.id = "ns:{0}/kind:{1}/name:{2}".format(ns_or_cluster_wide, kind, name)


def save_descriptors_to_dir(descriptors, directory, yaml_instance=YAML(typ="rt")):
    """save input descriptors to files in dir"""
    for id, desc in descriptors.items():
        output_file = os.path.join(directory, desc.subDir, desc.filename)
        with open(output_file, "wt") as out:
            yaml_instance.dump(desc.yaml_content, out)


def convert_input_to_descriptors(input_file, yaml_instance=YAML(typ="rt")):
    """convert input (file or STDIN) to a dict of descriptors"""
    if input_file is not None:
        with open(input_file, "rt") as f_input:
            parsed = yaml_instance.load_all(f_input.read())
    else:
        parsed = yaml_instance.load_all(sys.stdin.read())
    descriptors = {}
    try:
        # Read the parsed content to force the scanner to issue errors if any
        for resource in parsed:
            resource_name = resource["metadata"]["name"]
            resource_kind = resource["kind"]
            if "namespace" in resource["metadata"]:
                resource_namespace = resource["metadata"]["namespace"]
            else:
                resource_namespace = None
            k8s_descriptor = K8SDescriptor(
                resource_name, resource_kind, resource_namespace, resource
            )
            descriptors[k8s_descriptor.id] = k8s_descriptor
    except ScannerError as e:
        print("Something is wrong in the input file, got error from Scanner")
        print(e)
        return
    return descriptors


def old():
    with open("samples/input-1.yml", "rt") as f_input:
        documents = yaml.load_all(f_input.read())
        for resource in documents:
            # yaml.dump(resource, sys.stdout)
            ns = ""
            if "namespace" in resource["metadata"]:
                ns = "{0}/".format(resource["metadata"]["namespace"])
            print(
                "{0}{1}--{2}.yml".format(
                    ns,
                    resource["kind"].lower(),
                    resource["metadata"]["name"].lower().replace(":", "-"),
                )
            )


def main():
    """(re)format yaml"""
    yaml = YAML(typ="rt")
    descriptors = convert_input_to_descriptors("samples/input-1.yml", yaml)
    for id, desc in descriptors.items():
        print(id)


if __name__ == "__main__":
    main()
