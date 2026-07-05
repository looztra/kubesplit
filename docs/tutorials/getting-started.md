# Getting started with Kubesplit

This tutorial walks you through installing `kubesplit` and splitting your first multidoc Kubernetes manifest. At the end, you will know how to run `kubesplit` on a file and read the tree of files it generates.

## Step 1: Install kubesplit

`Kubesplit` is published on [pypi.org](https://pypi.org/project/kubesplit/). Install it as a standalone tool with [uv](https://docs.astral.sh/uv/guides/tools/):

```shell
uv tool install kubesplit
```

Check that it works:

```shell
kubesplit --version
```

You should see the kubesplit version, along with the version of [yamkix](https://github.com/looztra/yamkix) it embeds:

```text
kubesplit v0.5.0 (yamkix v0.16.0)
```

Other installation methods (`pip`, Docker, `mise`) are described in the [installation how-to guide](../how-to/install.md).

## Step 2: Create a manifest to split

Create a file named `all-in-one.yml` holding two resources in a single multidoc stream:

```yaml
---
apiVersion: v1
kind: Namespace
metadata:
  name: demo
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: demo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: web
          image: nginx:1.27
```

## Step 3: Split it

Run `kubesplit`, pointing `--input` at the file and `--output` at a directory that does not need to exist yet:

```shell
kubesplit --input all-in-one.yml --output out
```

`kubesplit` prints its configuration and a short summary to `stderr`:

```text
[kubesplit(0.5.0)] Processing: input=all-in-one.yml, output_dir=out, clean_output_dir=False, prefix_resource_files=True, typ=rt, ...
Found [2] valid / [0] lists / [0] invalid / [0] empty resources
```

## Step 4: Look at what was generated

```shell
tree --dirsfirst out
```

```text
out
├── demo
│   └── 20--deployment--web.yml
└── 00--namespace--demo.yml

2 directories, 2 files
```

Notice what happened:

- The **cluster-wide** `Namespace` resource landed at the root of the output directory.
- The **namespaced** `Deployment` landed in a `demo/` subdirectory named after its namespace.
- Each file is named `<order-prefix>--<kind>--<name>.yml`. The `00` / `20` prefixes impose a natural apply order (namespaces before deployments) — see [file naming and layout](../reference/file-naming.md).
- Each file was reformatted with kubesplit's opinionated YAML style (explicit `---` start, comments preserved).

## Where to go next

- Learn all the ways to feed input and control the output directory in [Split descriptors](../how-to/split-descriptors.md).
- Change how files are named and grouped in [Organize the output](../how-to/organize-output.md).
- Pipe `kustomize build` or `helm template` straight into kubesplit with [Use with Kustomize and Helm](../how-to/integrate-kustomize-helm.md).
- Understand the resource detection and ordering logic in [How kubesplit works](../explanation/how-it-works.md).
