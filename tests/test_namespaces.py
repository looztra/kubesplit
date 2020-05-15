"""Tests for `kubesplit` package."""

from kubesplit.k8s_descriptor import K8SDescriptor
from kubesplit.namespaces import get_all_namespaces


def test_get_all_namespace():
    """test_get_all_namespace."""
    descriptors = dict()
    k8s_default_svc_dummy = K8SDescriptor(
        name="dummy", kind="Service", namespace="default", as_yaml=""
    )
    k8s_default_svc_dummy2 = K8SDescriptor(
        name="dummy2", kind="Service", namespace="default", as_yaml=""
    )
    k8s_ns1_deploy_foo = K8SDescriptor(
        name="foo", kind="Deployment", namespace="ns1", as_yaml=""
    )
    k8s_ns2_deploy_foo = K8SDescriptor(
        name="foo", kind="Deployment", namespace="ns2", as_yaml=""
    )
    descriptors[k8s_default_svc_dummy.id] = k8s_default_svc_dummy
    descriptors[k8s_default_svc_dummy2.id] = k8s_default_svc_dummy2
    descriptors[k8s_ns1_deploy_foo.id] = k8s_ns1_deploy_foo
    descriptors[k8s_ns2_deploy_foo.id] = k8s_ns2_deploy_foo
    res = get_all_namespaces(descriptors)
    assert len(res) == 3
    assert "default" in res
    assert "ns1" in res
    assert "ns2" in res


def test_get_all_namespace_when_no_descriptors():
    """test_get_all_namespace_when_no_descriptors."""
    descriptors = dict()
    res = get_all_namespaces(descriptors)
    assert len(res) == 0
