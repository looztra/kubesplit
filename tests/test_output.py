"""Test the output package."""
from io import StringIO

from yamkix.config import get_yamkix_config_from_default
from yamkix.yaml_writer import get_opinionated_yaml_writer

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
    yamkix_config = get_yamkix_config_from_default(quotes_preserved=True)
    yaml_instance = get_opinionated_yaml_writer(yamkix_config)
    parsed = yaml_instance.load_all(s_input)
    for yaml_resource in parsed:
        as_yaml = yaml_resource
    descriptor = K8SDescriptor(
        name="tname", kind="ReplicaSet", namespace="tns", as_yaml=as_yaml
    )
    output = StringIO()
    save_descriptor_to_stream(
        descriptor,
        output,
        yaml_instance=yaml_instance,
        yamkix_config=yamkix_config,
    )
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
    yamkix_config = get_yamkix_config_from_default(quotes_preserved=False)
    yaml_instance = get_opinionated_yaml_writer(yamkix_config)
    parsed = yaml_instance.load_all(s_input)
    for yaml_resource in parsed:
        as_yaml = yaml_resource
    descriptor = K8SDescriptor(
        name="tname", kind="ReplicaSet", namespace="tns", as_yaml=as_yaml
    )
    output = StringIO()
    save_descriptor_to_stream(
        descriptor, output, yaml_instance, yamkix_config=yamkix_config
    )
    s_output = output.getvalue()
    print("input    => [{0}]".format(s_input))
    print("expected => [{0}]".format(s_expected))
    print("output   => [{0}]".format(s_output))
    assert s_output == s_expected


def test_roundtrip_when_dash_inwards_false():
    """test_roundtrip_when_dash_inwards_false."""
    s_input = """---
apiVersion: v1 # with comment
kind: Pod
metadata:
  name: yan_solo
  namespace: tatouine
spec:
  containers:
  - name : first
    image: nginx
    ports:
    - name: http
      port: 80
    - name: https
      port: 443
"""
    s_expected = """---
apiVersion: v1 # with comment
kind: Pod
metadata:
  name: yan_solo
  namespace: tatouine
spec:
  containers:
  - name: first
    image: nginx
    ports:
    - name: http
      port: 80
    - name: https
      port: 443
"""
    yamkix_config = get_yamkix_config_from_default(dash_inwards=False)
    yaml_instance = get_opinionated_yaml_writer(yamkix_config)
    parsed = yaml_instance.load_all(s_input)
    for yaml_resource in parsed:
        as_yaml = yaml_resource
    descriptor = K8SDescriptor(
        name="tname", kind="ReplicaSet", namespace="tns", as_yaml=as_yaml
    )
    output = StringIO()
    save_descriptor_to_stream(
        descriptor, output, yaml_instance, yamkix_config=yamkix_config
    )
    s_output = output.getvalue()
    print("input    => [{0}]".format(s_input))
    print("expected => [{0}]".format(s_expected))
    print("output   => [{0}]".format(s_output))
    assert s_output == s_expected


def test_roundtrip_when_dash_inwards_true():
    """test_roundtrip_when_dash_inwards_true."""
    s_input = """---
apiVersion: v1 # with comment
kind: Pod
metadata:
  name: yan_solo
  namespace: tatouine
spec:
  containers:
  - name : first
    image: nginx
    ports:
    - name: http
      port: 80
    - name: https
      port: 443
"""
    s_expected = """---
apiVersion: v1 # with comment
kind: Pod
metadata:
  name: yan_solo
  namespace: tatouine
spec:
  containers:
    - name: first
      image: nginx
      ports:
        - name: http
          port: 80
        - name: https
          port: 443
"""
    yamkix_config = get_yamkix_config_from_default(dash_inwards=True)
    yaml_instance = get_opinionated_yaml_writer(yamkix_config)
    parsed = yaml_instance.load_all(s_input)
    for yaml_resource in parsed:
        as_yaml = yaml_resource
    descriptor = K8SDescriptor(
        name="tname", kind="ReplicaSet", namespace="tns", as_yaml=as_yaml
    )
    output = StringIO()
    save_descriptor_to_stream(
        descriptor, output, yaml_instance, yamkix_config=yamkix_config
    )
    s_output = output.getvalue()
    print("input    => [{0}]".format(s_input))
    print("expected => [{0}]".format(s_expected))
    print("output   => [{0}]".format(s_output))
    assert s_output == s_expected


def test_roundtrip_with_unconsistent_comments():
    """test_roundtrip_with_unconsistent_comments.

    Comments badly placed should be pushed to 1 char after content
    """
    s_input = """---
apiVersion: v1    # with comment
kind: Pod
metadata:
  name: yan_solo
  namespace: tatouine
spec:
  containers:
  - name : first
    image: nginx
    ports:
    - name: http
      port: 80
    - name: https
      port: 443
"""
    s_expected = """---
apiVersion: v1 # with comment
kind: Pod
metadata:
  name: yan_solo
  namespace: tatouine
spec:
  containers:
    - name: first
      image: nginx
      ports:
        - name: http
          port: 80
        - name: https
          port: 443
"""
    yamkix_config = get_yamkix_config_from_default(spaces_before_comment=1)
    yaml_instance = get_opinionated_yaml_writer(yamkix_config)
    parsed = yaml_instance.load_all(s_input)
    for yaml_resource in parsed:
        as_yaml = yaml_resource
    descriptor = K8SDescriptor(
        name="tname", kind="ReplicaSet", namespace="tns", as_yaml=as_yaml
    )
    output = StringIO()
    save_descriptor_to_stream(
        descriptor, output, yaml_instance, yamkix_config=yamkix_config
    )
    s_output = output.getvalue()
    print("input    => [{0}]".format(s_input))
    print("expected => [{0}]".format(s_expected))
    print("output   => [{0}]".format(s_output))
    assert s_output == s_expected


def test_roundtrip_with_weird_comments_config():
    """test_roundtrip_with_weird_comments_config."""
    s_input = """---
apiVersion: v1    # with comment
kind: Pod
metadata:
  name: yan_solo
  namespace: tatouine
spec:
  containers:
  - name : first
    image: nginx
    ports:
    - name: http
      port: 80
    - name: https
      port: 443
"""
    s_expected = """---
apiVersion: v1       # with comment
kind: Pod
metadata:
  name: yan_solo
  namespace: tatouine
spec:
  containers:
    - name: first
      image: nginx
      ports:
        - name: http
          port: 80
        - name: https
          port: 443
"""
    yamkix_config = get_yamkix_config_from_default(spaces_before_comment=7)
    yaml_instance = get_opinionated_yaml_writer(yamkix_config)
    parsed = yaml_instance.load_all(s_input)
    for yaml_resource in parsed:
        as_yaml = yaml_resource
    descriptor = K8SDescriptor(
        name="tname", kind="ReplicaSet", namespace="tns", as_yaml=as_yaml
    )
    output = StringIO()
    save_descriptor_to_stream(
        descriptor, output, yaml_instance, yamkix_config=yamkix_config
    )
    s_output = output.getvalue()
    print("input    => [{0}]".format(s_input))
    print("expected => [{0}]".format(s_expected))
    print("output   => [{0}]".format(s_output))
    assert s_output == s_expected
