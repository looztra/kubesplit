#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `kubesplit` package."""
from io import StringIO
from ruamel.yaml import YAML
from kubesplit.k8s_descriptor import K8SDescriptor
from kubesplit.kubesplit import (
    get_all_namespaces,
    convert_input_to_descriptors,
    save_descriptor_to_stream,
)


def test_get_all_namespace():
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
    descriptors = dict()
    res = get_all_namespaces(descriptors)
    assert len(res) == 0


def test_convert_input_to_descriptors():
    sut = StringIO()
    sut.write(
        """---
apiVersion: extensions/v1beta1 # with comment
kind: ReplicaSet
metadata:
  name: frontend
  namespace: yolo
  annotations:
    boubou: frontend
spec:
  replicas: 2
  selector:
    matchExpressions:
      - key: env
        operator: "In"
        values: ["int", "rd"]
    matchLabels:
      app: frontend
  template:
    metadata:
      name: frontend
      labels:
        app: frontend
        env: int
    spec:
      containers:
        - name: nginx-fe-4-rs
          image: nginx:stable-alpine
          ports:
            - containerPort: 80
"""
    )
    sut.seek(0)
    res = convert_input_to_descriptors(sut)
    assert len(res) == 1
    k = next(iter(res))
    assert res[k].name == "frontend"
    assert res[k].kind == "ReplicaSet"
    assert res[k].namespace == "yolo"


def test_convert_input_to_descriptors_when_input_is_empty():
    sut = StringIO()
    sut.write(
        """---
"""
    )
    sut.seek(0)
    res = convert_input_to_descriptors(sut)
    assert len(res) == 0


def test_convert_input_to_descriptors_when_input_is_invalid_no_metadata():
    sut = StringIO()
    sut.write(
        """---
apiVersion: extensions/v1beta1 # with comment
kind: ReplicaSet
"""
    )
    sut.seek(0)
    res = convert_input_to_descriptors(sut)
    assert len(res) == 0


def test_convert_input_to_descriptors_when_input_is_invalid_no_kind():
    sut = StringIO()
    sut.write(
        """---
apiVersion: extensions/v1beta1 # with comment
metadata:
  name: frontend
  namespace: yolo
  annotations:
    boubou: frontend

"""
    )
    sut.seek(0)
    res = convert_input_to_descriptors(sut)
    assert len(res) == 0


def test_convert_input_to_descriptors_when_input_is_invalid_no_name():
    sut = StringIO()
    sut.write(
        """---
apiVersion: extensions/v1beta1 # with comment
kind: ReplicaSet
metadata:
  namespace: yolo
  annotations:
    boubou: frontend

"""
    )
    sut.seek(0)
    res = convert_input_to_descriptors(sut)
    assert len(res) == 0


def test_convert_input_to_descriptors_when_content_is_mixed():
    sut = StringIO()
    sut.write(
        """---
apiVersion: extensions/v1beta1 # with comment
kind: ReplicaSet
metadata:
  name: frontend
  namespace: yolo
  annotations:
    boubou: frontend
spec:
  replicas: 2
  selector:
    matchExpressions:
      - key: env
        operator: "In"
        values: ["int", "rd"]
    matchLabels:
      app: frontend
  template:
    metadata:
      name: frontend
      labels:
        app: frontend
        env: int
    spec:
      containers:
        - name: nginx-fe-4-rs
          image: nginx:stable-alpine
          ports:
            - containerPort: 80
---
---
apiVersion: extensions/v1beta1 # with comment
kind: ReplicaSet
metadata:
  name: bididididi
  namespace: akira
  annotations:
    boubou: frontend
---
apiVersion: extensions/v1beta1 # with comment
metadata:
  name: bididididi
  namespace: akira
  annotations:
    boubou: frontend

"""
    )
    sut.seek(0)
    res = convert_input_to_descriptors(sut)
    assert len(res) == 2


def test_convert_input_to_descriptors_when_content_has_no_namespace():
    sut = StringIO()
    sut.write(
        """---
apiVersion: v1
kind: Namespace
metadata:
  annotations:
    qima.com/generated-by: kustomize
    qima.com/kustomize-component: namespaces/demo
  labels:
    qima.com/editors: ci
  name: apps-demo
"""
    )
    sut.seek(0)
    res = convert_input_to_descriptors(sut)
    k = next(iter(res))
    assert len(res) == 1
    assert res[k].name == "apps-demo"
    assert res[k].kind == "Namespace"
    assert res[k].namespace is None


def test_roundtrip_when_preserve_quotes_true():
    s_input = """---
apiVersion: extensions/v1beta1 # with comment
kind: ReplicaSet
metadata:
  name: tname
  namespace: tns
  annotations:
    string_no_quotes: frontend
    string_single_quotes: 'frontend'
    string_double_quotes: "frontend"
    boolean_no_quotes: true
    boolean_single_quotes: 'true'
    boolean_double_quotes: "true"
    number_no_quotes: 1
    number_single_quotes: '1'
    number_double_quotes: "1"
"""
    yaml = YAML(typ="rt")
    yaml.explicit_start = True
    yaml.explicit_end = False
    yaml.preserve_quotes = True
    parsed = yaml.load_all(s_input)
    for y in parsed:
        as_yaml = y
    descriptor = K8SDescriptor(
        name="tname", kind="ReplicaSet", namespace="tns", as_yaml=as_yaml
    )
    output = StringIO()
    save_descriptor_to_stream(descriptor, output, yaml)
    s_output = output.getvalue()
    print("input  => [{0}]".format(s_input))
    print("output => [{0}]".format(s_output))
    assert s_output == s_input


def test_roundtrip_when_preserve_quotes_false():
    s_input = """---
apiVersion: extensions/v1beta1 # with comment
kind: ReplicaSet
metadata:
  name: tname
  namespace: tns
  annotations:
    string_no_quotes: frontend
    string_single_quotes: 'frontend'
    string_double_quotes: "frontend"
    boolean_no_quotes: true
    boolean_single_quotes: 'true'
    boolean_double_quotes: "true"
    number_no_quotes: 1
    number_single_quotes: '1'
    number_double_quotes: "1"
"""
    s_expected = """---
apiVersion: extensions/v1beta1 # with comment
kind: ReplicaSet
metadata:
  name: tname
  namespace: tns
  annotations:
    string_no_quotes: frontend
    string_single_quotes: frontend
    string_double_quotes: frontend
    boolean_no_quotes: true
    boolean_single_quotes: 'true'
    boolean_double_quotes: 'true'
    number_no_quotes: 1
    number_single_quotes: '1'
    number_double_quotes: '1'
"""
    yaml = YAML(typ="rt")
    yaml.explicit_start = True
    yaml.explicit_end = False
    yaml.preserve_quotes = False
    parsed = yaml.load_all(s_input)
    for y in parsed:
        as_yaml = y
    descriptor = K8SDescriptor(
        name="tname", kind="ReplicaSet", namespace="tns", as_yaml=as_yaml
    )
    output = StringIO()
    save_descriptor_to_stream(descriptor, output, yaml)
    s_output = output.getvalue()
    print("input    => [{0}]".format(s_input))
    print("expected => [{0}]".format(s_expected))
    print("output   => [{0}]".format(s_output))
    assert s_output == s_expected
