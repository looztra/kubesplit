"""Deal with namespaces."""

import logging
from pathlib import Path

from kubesplit.k8s_descriptor import K8SDescriptor


def get_all_namespaces(descriptors: dict[str, K8SDescriptor]) -> set[str]:
    """get_all_namespaces."""
    all_namespaces = set()
    for descriptor in descriptors.values():
        if descriptor.has_namespace():
            all_namespaces.add(descriptor.compute_namespace_dirname())
    return all_namespaces


def prepare_namespace_directories(root_directory: Path, namespaces: set[str]) -> None:
    """prepare_namespace_directories."""
    for namespace in namespaces:
        ns_dir = root_directory / namespace
        if not ns_dir.exists():
            logging.info("Creating directory [%s]", ns_dir)
            ns_dir.mkdir(parents=True)
