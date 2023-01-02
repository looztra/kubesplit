# kubesplit

[![Pypi](https://img.shields.io/pypi/v/kubesplit.svg)](https://pypi.python.org/pypi/kubesplit)

## What?

[<img src="https://img.shields.io/pypi/v/kubesplit.svg">](https://pypi.python.org/pypi/kubesplit)

Split multidoc yaml formatted [kubernetes](https://kubernetes.io/) descriptors to a set of single resource files.

If you just want an opinionated yaml formatter, you can have a look at [yamkix](https://github.com/looztra/yamkix).

## Installation

### The pip way

```bash
# Install/Update
pip3 install -U --user kubesplit
# Enjoy
kubesplit -i path/to/yaml_file.yml -o path/to/output/directory
# or
cat path/to/yaml_file.yml | kubesplit -o path/to/output/directory

```

### The docker way

```bash
# Use latest
docker image pull looztra/kubesplit
# Or one of the version+sha1 related tags
docker image pull looztra/kubesplit:[version]-[sha1]
# Enjoy
docker container run \
        -ti --rm \
        -v $(pwd):/code \
        -w /code looztra/kubesplit \
        -i path/to/yaml_file.yml \
        -o path/to/output/directory
# or
cat path/to/yaml_file.yml | \
        docker container run \
        -ti --rm \
        -v $(pwd):/code \
        -w /code looztra/kubesplit \
        -o path/to/output/directory
```

All tags available at <https://cloud.docker.com/repository/docker/looztra/kubesplit/tags>

## Usage

```bash
╰(.venv)─» kubesplit -h
usage: kubesplit [-h] [-i INPUT] [-t TYP] -o OUTPUT_DIR [-n] [-e] [-q] [-f]
        [-d] [-c] [-p]

Split a set of Kubernetes descriptors to a set of files. The yaml format of
the generated files can be tuned using the same parameters as the one used by
Yamkix. By default, explicit_start is `On`, explicit_end is `Off` and array
elements are pushed inwards the start of the matching sequence. Comments are
preserved thanks to default parsing mode `rt`.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        the file to parse, or STDIN if not specified or if
                        value is -
  -t TYP, --typ TYP     the yaml parser mode. Can be `safe` or `rt`
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        the name of the output target directory. The target
                        directory will be created if it does not exist if it's
                        possible
  -n, --no-explicit-start
                        by default, explicit start (---) of the yaml doc is
                        `On`, you can disable it with this option
  -e, --explicit-end    by default, explicit end (...) of the yaml doc is
                        `Off`, you can enable it with this option
  -q, --no-quotes-preserved
                        by default, quotes are preserved you can disable this
                        with this option
  -f, --default-flow-style
                        enable the default flow style `Off` by default. In
                        default flow style (with typ=`rt`), maps and lists are
                        written like json
  -d, --no-dash-inwards
                        by default, dash are pushed inwards use `--no-dash-
                        inwards` to have the dash start at the sequence level
  -c, --clean-output-dir
                        clean the output directory (rmtree) if set (default is
                        False)
  -p, --no-resource-prefix
                        by default, resource files are number prefixed, you
                        can disable this behaviour with this flag

```

## Features

- Invalid Kubernetes resources are ignored
- Empty resources are ignored
- Each resource found in the input is stored in a file with a name reflecting the name of the resource and its _kubernetes_ kind
- Cluster-wide resources (namespaces, clusterroles, clusterrolebindings) are stored in the root directory of the output, namespaced resources are stored in a subdirectory named like the namespace
- By default, resources are prefixed, use `--no-resource-prefix` to disable order prefixes
- By default, quotes are preserved, use `--no-quotes-preserved` to disable quotes unless needed (for boolean and numbers if they were provided in the input as for the moment Kubesplit is not aware of the fact that only kubernetes annotations and environment variables require string)
- By default, dash elements in list are pushed inwards, you can disable this behaviour with the `-d`/`--no-dash-inwards` option
- Comments are preserved
- The output directory will be created if it doesn't exist (if the user running the command as sufficient rights)
- You can clean (delete files and directories existing before running `kubesplit`) the output directory with the `-c`/`--clean-output-dir` (**use at your own risks**)

## Examples

You can find some input and output examples in the [test-assets](https://github.com/looztra/kubesplit/tree/master/test-assets) directory

### Valid resources, no quotes preserved

```bash
╰(.venv)─»  kubesplit --input test-assets/source/all-in-one.yml \
              --output test-assets/expected/all-in-one--no-quotes-preserved \
              --no-quotes-preserved \
              --clean-output-dir
Processing: input=test-assets/source/all-in-one.yml, output_dir=test-assets/expected/all-in-one--no-quotes-preserved, clean_output_dir=True, typ=rt, explicit_start=True, explicit_end=False, default_flow_style=False, quotes_preserved=False, dash_inwards=True, prefix_resource_files=True
Found [16] valid / [0] invalid / [0] empty resources

╰(.venv)─» tree --dirsfirst test-assets/expected/all-in-one--no-quotes-preserved
test-assets/expected/all-in-one--no-quotes-preserved
├── apps-demo
│   └── 05--rolebinding--example-ns-demo-developer-binding.yml
├── apps-integration
│   └── 05--rolebinding--example-ns-integration-developer-binding.yml
├── ingress-controllers
│   ├── 03--serviceaccount--traefik-ingress-controller.yml
│   ├── 11--configmap--traefik-conf.yml
│   ├── 12--persistentvolumeclaim--traefik-acme.yml
│   ├── 20--deployment--traefik-ingress-controller.yml
│   ├── 30--service--traefik-ingress-endpoint.yml
│   ├── 30--service--traefik-web-ui.yml
│   └── 31--ingress--traefik-web-ui.yml
├── 00--namespace--apps-demo.yml
├── 00--namespace--apps-integration.yml
├── 00--namespace--ingress-controllers.yml
├── 01--clusterrole--example-node-viewer.yml
├── 01--clusterrole--example-traefik-ingress-controller.yml
├── 02--clusterrolebinding--example-node-viewer-developer.yml
└── 02--clusterrolebinding--example-traefik-ingress-controller.yml

3 directories, 16 files
```

### Valid resources, no prefix, no quotes preserved

```bash
╰(.venv)─» kubesplit --input test-assets/source/all-in-one.yml \
              --output test-assets/expected/all-in-one--no-quotes-preserved--no-resource-prefix \
              --no-quotes-preserved \
              --no-resource-prefix \
              --clean-output-dir
Processing: input=test-assets/source/all-in-one.yml, output_dir=test-assets/expected/all-in-one--no-quotes-preserved--no-resource-prefix, clean_output_dir=True, typ=rt, explicit_start=True, explicit_end=False, default_flow_style=False, quotes_preserved=False, dash_inwards=True, prefix_resource_files=False
Found [16] valid / [0] invalid / [0] empty resources

╰(.venv)─» tree --dirsfirst test-assets/expected/all-in-one--no-quotes-preserved--no-resource-prefix
test-assets/expected/all-in-one--no-quotes-preserved--no-resource-prefix
├── apps-demo
│   └── rolebinding--example-ns-demo-developer-binding.yml
├── apps-integration
│   └── rolebinding--example-ns-integration-developer-binding.yml
├── ingress-controllers
│   ├── configmap--traefik-conf.yml
│   ├── deployment--traefik-ingress-controller.yml
│   ├── ingress--traefik-web-ui.yml
│   ├── persistentvolumeclaim--traefik-acme.yml
│   ├── serviceaccount--traefik-ingress-controller.yml
│   ├── service--traefik-ingress-endpoint.yml
│   └── service--traefik-web-ui.yml
├── clusterrolebinding--example-node-viewer-developer.yml
├── clusterrolebinding--example-traefik-ingress-controller.yml
├── clusterrole--example-node-viewer.yml
├── clusterrole--example-traefik-ingress-controller.yml
├── namespace--apps-demo.yml
├── namespace--apps-integration.yml
└── namespace--ingress-controllers.yml

3 directories, 16 files
```

### Mixed content : valid, invalid and empty resources, no quotes preserved

```bash
╰(.venv)─» kubesplit --input test-assets/source/mixed-content-valid-invalid-and-empty-resources.yml \
                        --output test-assets/expected/mixed-content-valid-invalid-and-empty-resources--no-quotes-preserved \
                        --no-quotes-preserved \
                        --clean-output-dir
Processing: input=test-assets/source/mixed-content-valid-invalid-and-empty-resources.yml, output_dir=test-assets/expected/mixed-content-valid-invalid-and-empty-resources--no-quotes-preserved, clean_output_dir=True, typ=rt, explicit_start=True, explicit_end=False, default_flow_style=False, quotes_preserved=False, dash_inwards=True, prefix_resource_files=True
Found [2] valid / [1] invalid / [1] empty resources

╰(.venv)─» tree --dirsfirst test-assets/expected/mixed-content-valid-invalid-and-empty-resources--no-quotes-preserved
test-assets/expected/mixed-content-valid-invalid-and-empty-resources--no-quotes-preserved
├── akira
│   └── 25--replicaset--bididididi.yml
└── yolo
    └── 25--replicaset--frontend.yml

2 directories, 2 files

```

## Use cases

### With Kustomize

```bash
kustomize build overlays/prod | kubesplit -q -i - -o generated/prod

```

### With Helm

```bash
helm template --namespace target-ns --values config.yml my-chart | kubesplit -q -i - -o generated/prod

```

## To preserve or not to preserve quotes?

- _Quotes preserved_ means : if there were quotes in the input, they will also be present in the output, and it will be the same type (single/double) of quotes
- _Quotes not preserved_ means :
  - if quotes are not necessary (around _pure_ strings), they will be removed
  - if quotes are present around booleans and numbers, they will be converted to default (single quotes)
  - if quotes are not present around booleans and numbers, there will be no quotes in the output too

**Note**: there is no option for the moment to force the usage of double quotes when `-q`/`--no-quotes-preserved` is used.

### Quotes preserved (default behaviour)

With input :

```yaml
---
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
```

the ouput will be the same as the input :

```yaml
---
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

```

### Quotes not preserved (using `-q/--no-quotes-preserved`)

With input :

```yaml
---
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
```

the ouput will be :

```yaml
---
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

```

**Note** : `kubesplit` is not fully _Kubernetes_ aware for the moment, so it does not try to enforce this behaviour only on string sensible _kubernetes_ resource fields (`.metadata.annotations` and `.spec.containers.environment` values)

## TODO

- Provide an option to enforce the quote type (by default, with `--no-quotes-preserved` boolean and integers are forced with single quotes) Hint => <https://stackoverflow.com/questions/56588374/when-using-ruamel-yaml-and-preserve-quotes-true-is-there-a-way-to-force-roundtri/56592388#56592388>

## Contribute

```bash
# Setup a local virtual env (needed once)
python3 -m venv .venv
# Activate
source .venv/bin/activate.fish # <= adjust
# Install requirements
pip install -r requirements_dev.txt
# Run locally
python -m kubesplit -h
# All make targets
make
# Tests anyone?
make test
# hack hack
# push PR
```

## Credits

- This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
- Kubesplit uses the awesome [ruamel.yaml](https://yaml.readthedocs.io/en/latest/pyyaml.html) python lib.
- Dependencies scanned by [PyUp.io](https://pyup.io/)
