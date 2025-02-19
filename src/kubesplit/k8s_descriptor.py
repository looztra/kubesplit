"""Provides a wrapper for a Kubernetes descriptor."""

import os
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import ClassVar

from kubesplit.errors import K8SNamespaceError


@dataclass
class K8SDescriptor:
    """Kubernetes descriptor."""

    name: str
    kind: str
    namespace: str | None
    as_yaml: dict
    use_order_prefix: bool = True
    extension: str = "yml"
    is_list: bool = False

    _cluster_wide_str_rep: ClassVar[str] = "__clusterwide__"
    _order_prefixes: ClassVar[Mapping[str, str]] = MappingProxyType(
        {
            "namespace": "00",
            "clusterrole": "01",
            "clusterrolebinding": "02",
            "serviceaccount": "03",
            "role": "04",
            "rolebinding": "05",
            "secret": "10",
            "configmap": "11",
            "persistentvolumeclaim": "12",
            "persistentvolume": "13",
            "deployment": "20",
            "daemonset": "21",
            "statefulset": "22",
            "job": "23",
            "cronjob": "24",
            "replicaset": "25",
            "service": "30",
            "ingress": "31",
            "networkpolicy": "40",
            "poddisruptionbudget": "41",
            "priorityclass": "42",
            "__unknown__": "99",
        }
    )

    def __post_init__(
        self,
    ) -> None:
        """Init."""
        ns_or_cluster_wide = self.namespace if self.namespace is not None else K8SDescriptor._cluster_wide_str_rep
        self.id = f"ns:{ns_or_cluster_wide}/kind:{self.kind}/name:{self.name}"

    def has_namespace(self) -> bool:
        """has_namespace."""
        return self.namespace is not None

    def compute_namespace_dirname(self) -> str:
        """compute_namespace_dirname."""
        if self.namespace is not None:
            return self.namespace.lower()
        raise K8SNamespaceError

    def compute_filename(self) -> str:
        """compute_filename."""
        return f"{self.get_order_prefix()}{self.kind.lower()}--{self.name.lower().replace(':', '-')}.{self.extension}"

    def get_order_prefix(self) -> str:
        """get_order_prefix."""
        if self.use_order_prefix:
            k = self.kind.lower() if self.kind.lower() in K8SDescriptor._order_prefixes else "__unknown__"
            return f"{K8SDescriptor._order_prefixes[k]}--"
        return ""

    def compute_filename_with_namespace(self, root_directory) -> str:
        """compute_filename_with_namespace."""
        if self.has_namespace():
            return os.path.join(
                root_directory,
                self.compute_namespace_dirname(),
                self.compute_filename(),
            )
        return os.path.join(root_directory, self.compute_filename())
