#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `kubesplit` package."""
from kubesplit.k8s_descriptor import K8SDescriptor
from kubesplit.kubesplit import get_all_namespaces


def test_get_all_namespace():
    descriptors = dict()
    k8s_descriptor = K8SDescriptor(
        name="dummy", kind="Service", namespace="default", as_yaml=""
    )
    descriptors[k8s_descriptor.id] = k8s_descriptor
    res = get_all_namespaces(descriptors)
    assert len(res) == 1
