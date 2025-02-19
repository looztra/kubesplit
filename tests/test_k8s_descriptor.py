"""Test the K8SDescriptor wrapper."""

import pytest

from kubesplit.errors import K8SNamespaceError
from kubesplit.k8s_descriptor import K8SDescriptor

data_for_test_get_order_prefix = [
    ("Namespace"),
    ("ServiceAccount"),
    ("ClusterRole"),
    ("Role"),
    ("ClusterRoleBinding"),
    ("RoleBinding"),
    ("Deployment"),
    ("Service"),
    ("Ingress"),
    ("StatefulSet"),
]


def test_has_namespace_when_true() -> None:
    """test_has_namespace_when_true."""
    k8s_default_svc_dummy = K8SDescriptor(name="dummy", kind="Service", namespace="default", as_yaml={})
    assert k8s_default_svc_dummy.has_namespace()


def test_has_namespace_when_false() -> None:
    """test_has_namespace_when_false."""
    k8s_default_svc_dummy = K8SDescriptor(name="dummy", kind="Service", namespace=None, as_yaml={})
    assert not k8s_default_svc_dummy.has_namespace()


def test_compute_namespace_dirname_when_has_namespace() -> None:
    """test_compute_namespace_dirname_when_has_namespace."""
    k8s_default_svc_dummy = K8SDescriptor(name="dummy", kind="Service", namespace="default", as_yaml={})
    assert k8s_default_svc_dummy.compute_namespace_dirname() == "default"


def test_compute_namespace_dirname_when_no_namespace() -> None:
    """test_compute_namespace_dirname_when_no_namespace."""
    k8s_default_svc_dummy = K8SDescriptor(name="dummy", kind="Service", namespace=None, as_yaml={})
    with pytest.raises(K8SNamespaceError):
        k8s_default_svc_dummy.compute_namespace_dirname()


@pytest.mark.parametrize("kind", data_for_test_get_order_prefix)
def test_get_order_prefix(kind: str) -> None:
    """test_get_order_prefix."""
    sut = K8SDescriptor(
        name="for_test",
        kind=kind,
        namespace=None,
        as_yaml={},
        use_order_prefix=True,
    )
    assert (sut.get_order_prefix() == "") is False


@pytest.mark.parametrize("kind", data_for_test_get_order_prefix)
def test_get_order_prefix_when_disabled(kind: str) -> None:
    """test_get_order_prefix_when_disabled."""
    sut = K8SDescriptor(
        name="for_test",
        kind=kind,
        namespace=None,
        as_yaml={},
        use_order_prefix=False,
    )
    assert (sut.get_order_prefix() == "") is True


def test_is_list_with_default() -> None:
    """Test is_list with default."""
    sut = K8SDescriptor(
        name="for_test",
        kind="ConfigMap",
        namespace=None,
        as_yaml={},
        use_order_prefix=False,
    )
    assert sut.is_list is False


def test_is_list_can_be_set() -> None:
    """Test is_list with default."""
    sut = K8SDescriptor(
        name="for_test",
        kind="ConfigMapList",
        namespace=None,
        as_yaml={},
        use_order_prefix=False,
    )
    sut.is_list = True
    assert sut.is_list is True
