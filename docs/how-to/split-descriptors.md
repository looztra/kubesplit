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

## Check the console summary

While processing, kubesplit prints its resolved configuration and a resource count to `stderr`:

```text
[kubesplit(0.6.0)] Processing: input=all-in-one.yml, output_dir=out, clean_output_dir=True, prefix_resource_files=True, typ=rt, explicit_start=True, ...
Found [16] valid / [0] lists / [1] invalid / [2] empty resources
```

Verify that the **valid** count matches the number of resources you expect: invalid and empty documents are skipped silently, not written. What each count means is explained in [How kubesplit works](../explanation/how-it-works.md#how-each-document-is-classified).

## Troubleshooting

### The run fails and no files are written

The input contains a YAML syntax error. Kubesplit reports the parser error and produces **no** output rather than a partial result — fix the input (or the tool that renders it) and re-run.

### The `invalid` count is not zero

Some documents in the stream don't look like Kubernetes resources; they are skipped. If a resource you expected is missing from the output, check that it has both a `kind` and a `.metadata.name`.

## Next steps

- Change file names and grouping in [Organize the output](organize-output.md).
- Adjust the YAML style of the generated files in [Tune the YAML formatting](tune-yaml-formatting.md).
