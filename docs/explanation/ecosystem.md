# Ecosystem

This page situates `kubesplit` among the tools it works with and the tools it is built on.

## kubesplit vs yamkix

[yamkix](https://github.com/looztra/yamkix) is an opinionated YAML formatter: one YAML document in, the same document nicely formatted out. `kubesplit` is built **on top of** yamkix and adds the Kubernetes-specific concern of *splitting*: a multidoc stream in, many single-resource files out.

| | yamkix | kubesplit |
| --- | --- | --- |
| Input | a YAML file or `STDIN` | a multidoc Kubernetes stream or `STDIN` |
| Output | a formatted file or `STDOUT` | a **directory** of one-resource-per-file |
| Kubernetes-aware | no | partially (namespaces, kinds, ordering) |
| Formatting | its own opinionated rules | delegates to yamkix |

If you only need to format YAML, use yamkix. If you need to explode a Kubernetes render into reviewable files, use kubesplit — you still get yamkix formatting on every file.

## Where kubesplit fits in a Kubernetes workflow

Kubesplit reads from `STDIN`, so it composes with any tool that emits a multidoc stream:

- **Kustomize** — `kustomize build overlays/prod | kubesplit -i - -o generated/prod`
- **Helm** — `helm template … | kubesplit -i - -o generated/prod`
- **kubectl** — `kubectl kustomize … | kubesplit -i - -o generated/prod`

The typical motivation is **reviewability and GitOps**: instead of committing (or reviewing) one enormous rendered manifest, you commit a stable tree of small files. A change to one resource shows up as a change to one file, and the `NN--` [order prefixes](../reference/file-naming.md#order-prefixes) let `kubectl apply -f generated/ --recursive` apply resources in dependency order.

See [Use with Kustomize and Helm](../how-to/integrate-kustomize-helm.md) for ready-to-run pipelines.

## Built on

- [ruamel.yaml](https://yaml.readthedocs.io/) — the round-trip YAML parser that lets kubesplit preserve comments and quoting.
- [yamkix](https://github.com/looztra/yamkix) — the opinionated formatter applied to every generated file.
- [Typer](https://typer.tiangolo.com/) — the CLI framework.
