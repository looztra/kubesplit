"""Deal with namespaces."""

import logging
import os
from typing import Dict, Set

from kubesplit.k8s_descriptor import K8SDescriptor


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
