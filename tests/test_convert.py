"""Test the convert package."""
from io import StringIO

from ruamel.yaml import YAML

from kubesplit.convert import (
    convert_input_to_descriptors,
    resource_is_list,
    resource_is_object,
)

default_yaml = YAML(typ="rt")


def string_to_single_resource(resource_as_string):
    """Helper to convert a string to a resource."""
    resource_as_string.seek(0)
    return default_yaml.load(resource_as_string.read())


def test_resource_is_list_when_resource_is_empty():
    """Test resource_is_list when resource is empty."""
    string = StringIO()
    string.write(
        """---
"""
    )
    sut = string_to_single_resource(string)
    res = resource_is_list(sut)
    assert res is False


def test_resource_is_list_when_resource_is_not_a_list():
    """Test resource_is_list when resource is not a list."""
    string = StringIO()
    string.write(
        """---
apiVersion: extensions/v1beta1 # with comment
kind: ReplicaSet
"""
    )
    sut = string_to_single_resource(string)
    res = resource_is_list(sut)
    assert res is False


def test_resource_is_list_when_resource_is_a_list():
    """Test resource_is_list when resource is a list."""
    string = StringIO()
    string.write(
        """---
apiVersion: v1
items:
  - apiVersion: v1
    data:
      envoy.json: "some data"
    kind: ConfigMap
    metadata:
      name: grafana-dashboard-statefulset
      namespace: monitoring
  - apiVersion: v1
    data:
      envoy.json: "some data"
    kind: ConfigMap
    metadata:
      name: grafana-dashboard-statefulset2
      namespace: monitoring
kind: ConfigMapList
"""
    )
    sut = string_to_single_resource(string)
    res = resource_is_list(sut)
    assert res is True


def test_resource_is_list_when_resource_is_a_list_without_items():
    """Test resource_is_list when resource is a list without items."""
    string = StringIO()
    string.write(
        """---
apiVersion: v1
kind: ConfigMapList
"""
    )
    sut = string_to_single_resource(string)
    res = resource_is_list(sut)
    assert res is True


def test_resource_is_object_when_resource_is_a_list():
    """Test resource_is_object when resource is a list."""
    string = StringIO()
    string.write(
        """---
apiVersion: v1
items:
  - apiVersion: v1
    data:
      envoy.json: "some data"
    kind: ConfigMap
    metadata:
      name: grafana-dashboard-statefulset
      namespace: monitoring
  - apiVersion: v1
    data:
      envoy.json: "some data"
    kind: ConfigMap
    metadata:
      name: grafana-dashboard-statefulset2
      namespace: monitoring
kind: ConfigMapList
"""
    )
    sut = string_to_single_resource(string)
    res = resource_is_object(sut)
    assert res is False


def test_resource_is_object_when_resource_is_object():
    """Test resource_is_object when resource is object."""
    string = StringIO()
    string.write(
        """---
apiVersion: extensions/v1beta1 # with comment
kind: ReplicaSet
metadata:
  name: ze_super_replicaset
  annotations:
    nodevops.io/yamkix: rulez
"""
    )
    sut = string_to_single_resource(string)
    res = resource_is_object(sut)
    assert res is True


def test_resource_is_object_when_resource_is_empty():
    """Test resource_is_object when resource is empty."""
    string = StringIO()
    string.write(
        """---
"""
    )
    sut = string_to_single_resource(string)
    res = resource_is_object(sut)
    assert res is False


def test_convert_input_to_descriptors():
    """test_convert_input_to_descriptors."""
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
    """test_convert_input_to_descriptors_when_input_is_empty."""
    sut = StringIO()
    sut.write(
        """---
"""
    )
    sut.seek(0)
    res = convert_input_to_descriptors(sut)
    assert len(res) == 0


def test_convert_input_to_descriptors_when_input_is_invalid_no_metadata():
    """test_convert_input_to_descriptors_when_input_is_invalid_no_metadata."""
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
    """test_convert_input_to_descriptors_when_input_is_invalid_no_kind."""
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
    """test_convert_input_to_descriptors_when_input_is_invalid_no_name."""
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
    """test_convert_input_to_descriptors_when_content_is_mixed."""
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
    """test_convert_input_to_descriptors_when_content_has_no_namespace."""
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


def test_convert_input_to_descriptors_with_a_single_list():
    """test_convert_input_to_descriptors."""
    sut = StringIO()
    sut.write(
        """---
apiVersion: v1
items:
  - apiVersion: v1
    data:
      envoy.json: "some data"
    kind: ConfigMap
    metadata:
      name: grafana-dashboard-statefulset
      namespace: monitoring
  - apiVersion: v1
    data:
      envoy.json: "some data"
    kind: ConfigMap
    metadata:
      name: grafana-dashboard-statefulset2
      namespace: monitoring
kind: ConfigMapList
"""
    )
    sut.seek(0)
    res = convert_input_to_descriptors(sut)
    assert len(res) == 1
    k = next(iter(res))
    assert res[k].kind == "ConfigMapList"
    assert res[k].namespace is None
