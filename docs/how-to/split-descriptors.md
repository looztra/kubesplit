# Split descriptors

This guide shows the different ways to feed Kubernetes YAML to `kubesplit` and where the resulting files are written.

Unlike a formatter, `kubesplit` always writes to a **directory** (one file per resource), never to `STDOUT`. Check the available options with `kubesplit --help` (or see the [CLI options reference](../reference/cli.md)).

## Split a file

Use `-i/--input` for the source file and `-o/--output` for the target directory. The directory is created if it does not exist:

```shell
kubesplit --input all-in-one.yml --output out
```

`--output-dir` is an accepted alias of `--output`:

```shell
kubesplit --input all-in-one.yml --output-dir out
```

## Read from STDIN

If you omit `-i/--input`, or pass `-` as its value, `kubesplit` reads from `STDIN`. This is what makes it composable with `kustomize`, `helm`, `kubectl`, `cat`, etc.

```shell
# implicit STDIN
cat all-in-one.yml | kubesplit --output out

# explicit STDIN
cat all-in-one.yml | kubesplit --input - --output out
```

!!! note
    `-o/--output` is **mandatory**. There is no `STDOUT` mode because kubesplit produces many files, not a single stream. If you only want to reformat a single YAML document, use [yamkix](https://github.com/looztra/yamkix) instead.

## Reuse or clean the output directory

By default, kubesplit writes into the output directory **without removing anything that is already there**. Re-running on a changed input therefore leaves behind files for resources that no longer exist.

Use `-c/--clean-output-dir` to wipe the output directory (a full `rmtree`) before writing:

```shell
kubesplit --input all-in-one.yml --output out --clean-output-dir
```

!!! warning
    `--clean-output-dir` **recursively deletes** the target directory before regenerating it. Point it only at a directory you own and that contains nothing but generated output.

## Understand the console summary

While processing, kubesplit prints its resolved configuration and a resource count to `stderr`:

```text
[kubesplit(0.5.0)] Processing: input=all-in-one.yml, output_dir=out, clean_output_dir=True, prefix_resource_files=True, typ=rt, explicit_start=True, ...
Found [16] valid / [0] lists / [1] invalid / [2] empty resources
```

The counts tell you what kubesplit did with each document in the stream:

- **valid** — recognized single resources, one file each.
- **lists** — `*List` resources (e.g. `ConfigMapList`), written as a single file each (see [File naming and layout](../reference/file-naming.md#lists)).
- **invalid** — documents that don't look like Kubernetes resources; **ignored**.
- **empty** — empty documents (e.g. a trailing `---`); **ignored**.

## Next steps

- Change file names and grouping in [Organize the output](organize-output.md).
- Adjust the YAML style of the generated files in [Tune the YAML formatting](tune-yaml-formatting.md).
