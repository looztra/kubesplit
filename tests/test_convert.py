"""Test the convert package."""
from io import StringIO

from kubesplit.convert import convert_input_to_descriptors


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
