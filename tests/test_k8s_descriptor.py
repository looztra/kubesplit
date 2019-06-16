#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
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


def test_has_namespace_when_true():
    k8s_default_svc_dummy = K8SDescriptor(
        name="dummy", kind="Service", namespace="default", as_yaml=""
    )
    assert k8s_default_svc_dummy.has_namespace()


def test_has_namespace_when_false():
    k8s_default_svc_dummy = K8SDescriptor(
        name="dummy", kind="Service", namespace=None, as_yaml=""
    )
    assert not k8s_default_svc_dummy.has_namespace()


def test_compute_namespace_dirname_when_has_namespace():
    k8s_default_svc_dummy = K8SDescriptor(
        name="dummy", kind="Service", namespace="default", as_yaml=""
    )
    assert k8s_default_svc_dummy.compute_namespace_dirname() == "default"


def test_compute_namespace_dirname_when_no_namespace():
    k8s_default_svc_dummy = K8SDescriptor(
        name="dummy", kind="Service", namespace=None, as_yaml=""
    )
    assert k8s_default_svc_dummy.compute_namespace_dirname() is None


@pytest.mark.parametrize("kind", data_for_test_get_order_prefix)
def test_get_order_prefix(kind: str):
    d = K8SDescriptor(
        name="for_test",
        kind=kind,
        namespace=None,
        as_yaml=None,
        use_order_prefix=True,
    )
    assert (d.get_order_prefix() == "") is False


@pytest.mark.parametrize("kind", data_for_test_get_order_prefix)
def test_get_order_prefix_when_disabled(kind: str):
    d = K8SDescriptor(
        name="for_test",
        kind=kind,
        namespace=None,
        as_yaml=None,
        use_order_prefix=False,
    )
    assert (d.get_order_prefix() == "") is True
