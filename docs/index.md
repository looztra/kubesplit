# Kubesplit

`Kubesplit` splits a multidoc YAML file of [Kubernetes](https://kubernetes.io/) descriptors into a set of single-resource files, one file per resource, nicely formatted and organized by namespace.

It reads YAML from a file or `STDIN` and writes one file per resource into an output directory:

```text
all-in-one.yml  ──►  kubesplit  ──►  output-dir/
                                     ├── 00--namespace--apps-demo.yml
                                     ├── 01--clusterrole--example-node-viewer.yml
                                     └── ingress-controllers/
                                         ├── 20--deployment--traefik-ingress-controller.yml
                                         └── 30--service--traefik-web-ui.yml
```

## Why?

- Because a single `kustomize build` or `helm template` produces a giant multidoc stream that is hard to read and review.
- Because storing **one resource per file** — named after its kind and name, grouped by namespace — makes diffs, code reviews and GitOps repositories much easier to navigate.
- Because the generated files should be consistently formatted: `kubesplit` reuses [yamkix](https://github.com/looztra/yamkix) under the hood so every file follows the same opinionated YAML style.

If you just want an opinionated YAML formatter (without the Kubernetes splitting), have a look at [yamkix](https://github.com/looztra/yamkix) directly.

## Documentation

The documentation follows the [Diátaxis](https://diataxis.fr/) framework:

- **[Tutorials](tutorials/getting-started.md)** — start here if you are new: install kubesplit and split your first manifest.
- **How-to guides** — task-oriented recipes:
  [install](how-to/install.md),
  [split descriptors](how-to/split-descriptors.md),
  [organize the output](how-to/organize-output.md),
  [control quotes](how-to/control-quotes.md),
  [tune the YAML formatting](how-to/tune-yaml-formatting.md),
  [use with Kustomize and Helm](how-to/integrate-kustomize-helm.md).
- **Reference** — information-oriented descriptions:
  [CLI options](reference/cli.md),
  [file naming and layout](reference/file-naming.md),
  [public API](reference/api.md),
  [changelog](changelog.md).
- **Explanation** — understanding-oriented background:
  [how kubesplit works](explanation/how-it-works.md),
  [ecosystem](explanation/ecosystem.md).
