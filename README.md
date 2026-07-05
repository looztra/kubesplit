# kubesplit

[![Pypi](https://img.shields.io/pypi/v/kubesplit.svg)](https://pypi.python.org/pypi/kubesplit)
[![codecov](https://codecov.io/github/looztra/kubesplit/graph/badge.svg?token=ZK8IEI6VOS)](https://codecov.io/github/looztra/kubesplit)
[![Docs](https://img.shields.io/badge/docs-github.io-blue)](https://looztra.github.io/kubesplit/)

Split a multidoc YAML file of [Kubernetes](https://kubernetes.io/) descriptors into a set of single-resource files — one file per resource, nicely formatted and grouped by namespace.

If you just want an opinionated YAML formatter, have a look at [yamkix](https://github.com/looztra/yamkix).

## Documentation

📖 **Full documentation: <https://looztra.github.io/kubesplit/>**

It follows the [Diátaxis](https://diataxis.fr/) framework:

- [Getting started tutorial](https://looztra.github.io/kubesplit/tutorials/getting-started/)
- [How-to guides](https://looztra.github.io/kubesplit/how-to/split-descriptors/) (install, split, organize output, control quotes, Kustomize/Helm)
- [CLI reference](https://looztra.github.io/kubesplit/reference/cli/) and [file naming rules](https://looztra.github.io/kubesplit/reference/file-naming/)
- [How kubesplit works](https://looztra.github.io/kubesplit/explanation/how-it-works/)

## Quick start

```bash
# Install (see the docs for pip / Docker / mise alternatives)
uv tool install kubesplit

# Split a file into an output directory
kubesplit --input all-in-one.yml --output out

# Or read from STDIN (compose with kustomize / helm)
kustomize build overlays/prod | kubesplit -q -i - -o generated/prod
```

## Contributing

See the [contributing guide](https://looztra.github.io/kubesplit/contributing/).

## Credits

- Kubesplit uses the awesome [ruamel.yaml](https://yaml.readthedocs.io/) library and the [yamkix](https://github.com/looztra/yamkix) formatter.
