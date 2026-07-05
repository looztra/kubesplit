# How kubesplit works

This page explains what happens between "a multidoc YAML stream goes in" and "a tree of one-resource-per-file comes out". For task-oriented instructions, see the [how-to guides](../how-to/split-descriptors.md); for the exact naming rules, see [File naming and layout](../reference/file-naming.md).

## The pipeline

Kubesplit processes input in four stages:

1. **Prepare the output directory.** The target directory is created if missing. With `-c/--clean-output-dir`, it is first removed entirely and recreated.
2. **Parse the input.** The whole input (file or `STDIN`) is loaded as a multidoc stream with `ruamel.yaml` in the configured parsing mode (`rt` by default, so comments are preserved).
3. **Classify each document** into a descriptor (see below).
4. **Write one file per descriptor**, formatting each with [yamkix](https://github.com/looztra/yamkix) and placing it according to the [naming and layout rules](../reference/file-naming.md).

## How each document is classified

For every document in the stream, kubesplit decides what it is looking at:

- **Empty** — a document that parses to nothing (for example a stray trailing `---`). Counted as *empty* and **ignored**.
- **A resource** — a mapping that has both a `kind` and a `.metadata.name`. This is the common case: it becomes one output file.
- **A list** — a mapping whose `kind` ends with `List` and that has an `apiVersion`. It is written as a single file and **not** split into items (see [Lists](../reference/file-naming.md#lists)).
- **Invalid** — anything else (a mapping that isn't a recognizable resource or list). Counted as *invalid* and **ignored**.

The console line

```text
Found [16] valid / [0] lists / [1] invalid / [2] empty resources
```

is simply the tally of these four categories. Because invalid and empty documents are skipped rather than failing the run, you can safely pipe in a stream that contains comments-only documents or non-Kubernetes YAML.

!!! note
    If the parser hits a genuine syntax error (a `ScannerError`), kubesplit reports it and produces **no** output rather than a partial result.

## How the namespace and file name are chosen

Each recognized resource becomes a `K8SDescriptor` carrying its `name`, `kind`, and `namespace`:

- The **namespace** comes straight from `.metadata.namespace`. If it is absent, the resource is treated as **cluster-wide** and written to the root of the output directory. Kubesplit never guesses a namespace.
- The **file name** is derived from the `kind` and `name`, optionally prefixed with an order weight. The [order prefixes](../reference/file-naming.md#order-prefixes) are a fixed table keyed by `kind`, chosen so that lexical file order matches a sensible apply order (namespaces → RBAC → config/storage → workloads → networking).

Descriptors are keyed by an id built from `namespace + kind + name`, so two resources that differ only by namespace never collide, and a resource appearing twice in the input is de-duplicated (last one wins).

## Why kubesplit reuses yamkix

Kubesplit does not implement its own YAML writer. It formats every output file with [yamkix](https://github.com/looztra/yamkix), which is why the CLI exposes yamkix's styling options (`--no-explicit-start`, `--no-dash-inwards`, `--no-quotes-preserved`, `--line-width`, …). This keeps the two tools consistent: the formatting you get from `yamkix` on a single file is the formatting kubesplit gives each resource it extracts.

See the [Ecosystem](ecosystem.md) page for how kubesplit, yamkix, kustomize and helm fit together.

## Known limitations

- **Not fully Kubernetes-aware.** Quote handling (`-q`) applies to the whole document, not only to string-sensitive fields such as `.metadata.annotations` or container environment values.
- **Lists are not exploded.** `*List` resources are written as a single file rather than one file per item.
- **`--clean-output-dir` is destructive.** It recursively deletes the output directory before writing.
