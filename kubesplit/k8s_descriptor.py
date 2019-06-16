import os


class K8SDescriptor:
    """Kubernetes descriptor"""

    _cluster_wide_str_rep = "__clusterwide__"
    _order_prefixes = {
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
    }

    def __init__(
        self,
        name: str,
        kind: str,
        namespace: str,
        as_yaml,
        use_order_prefix: bool = True,
        extension: str = "yml",
    ):
        self.name = name
        self.kind = kind
        self.namespace = namespace
        self.as_yaml = as_yaml
        self.use_order_prefix = use_order_prefix
        self.extension = extension
        if namespace is None:
            ns_or_cluster_wide = K8SDescriptor._cluster_wide_str_rep
        else:
            ns_or_cluster_wide = namespace
        self.id = "ns:{0}/kind:{1}/name:{2}".format(
            ns_or_cluster_wide, kind, name
        )

    def has_namespace(self) -> bool:
        return self.namespace is not None

    def compute_namespace_dirname(self) -> str:
        if self.has_namespace():
            return self.namespace.lower()
        else:
            return None

    def compute_filename(self) -> str:
        return "{0}{1}--{2}.{3}".format(
            self.get_order_prefix(),
            self.kind.lower(),
            self.name.lower().replace(":", "-"),
            self.extension,
        )

    def get_order_prefix(self) -> str:
        if self.use_order_prefix:
            if self.kind.lower() in K8SDescriptor._order_prefixes:
                return "{0}--".format(
                    K8SDescriptor._order_prefixes[self.kind.lower()]
                )
            else:
                return "99--"
        else:
            return ""

    def compute_filename_with_namespace(self, root_directory) -> str:
        if self.has_namespace():
            return os.path.join(
                root_directory,
                self.compute_namespace_dirname(),
                self.compute_filename(),
            )
        else:
            return os.path.join(root_directory, self.compute_filename())
