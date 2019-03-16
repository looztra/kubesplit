#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `kubesplit` package."""
from kubesplit.k8s_descriptor import K8SDescriptor


def test_has_namespace_when_true():
    k8s_default_svc_dummy = K8SDescriptor(
        name="dummy", kind="Service", namespace="default", as_yaml=""
    )
    assert k8s_default_svc_dummy.hasNamespace()


def test_has_namespace_when_false():
    k8s_default_svc_dummy = K8SDescriptor(
        name="dummy", kind="Service", namespace=None, as_yaml=""
    )
    assert not k8s_default_svc_dummy.hasNamespace()


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
