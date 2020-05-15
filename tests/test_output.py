"""Test the output package."""
from io import StringIO

from ruamel.yaml import YAML

from kubesplit.k8s_descriptor import K8SDescriptor
from kubesplit.output import save_descriptor_to_stream


def test_roundtrip_when_preserve_quotes_true():
    """test_roundtrip_when_preserve_quotes_true."""
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
    """test_roundtrip_when_preserve_quotes_false."""
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
