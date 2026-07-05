# Tune the YAML formatting

Every file `kubesplit` writes is formatted by [yamkix](https://github.com/looztra/yamkix). The same yamkix styling options are exposed on the `kubesplit` CLI, so you can control exactly what the generated YAML looks like.

For quote handling specifically, see [Control quotes](control-quotes.md). For the full option list, see the [CLI options reference](../reference/cli.md).

## Document start and end markers

- Explicit start (`---`) is **on** by default. Disable it with `-n/--no-explicit-start`.
- Explicit end (`...`) is **off** by default. Enable it with `-e/--explicit-end`.

```shell
# no leading '---', add a trailing '...'
kubesplit --input all-in-one.yml --output out --no-explicit-start --explicit-end
```

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: demo
...
```

## Sequence indentation (dash inwards)

By default, dashes in sequences are pushed **inwards** (indented under their key). Use `-d/--no-dash-inwards` to keep them at the sequence level.

Default (`dash_inwards` on):

```yaml
spec:
  containers:
    - name: web
      image: nginx:1.27
```

With `--no-dash-inwards`:

```yaml
spec:
  containers:
  - name: web
    image: nginx:1.27
```

## Flow style vs block style

`kubesplit` emits block style by default. Enable YAML flow style (JSON-like `{}`/`[]`) with `-f/--default-flow-style`:

```shell
kubesplit --input all-in-one.yml --output out --default-flow-style
```

!!! note
    In the default `rt` (round-trip) parsing mode, `ruamel.yaml` remembers the style of each collection it parsed, so `--default-flow-style` mostly affects collections that carry no such memory. Existing block-style content generally stays block style.

## Force block style everywhere (`--enforce-block-style`)

Because `rt` mode remembers the original style, an input that already contains inline (flow-style) collections keeps them. Use `-B/--enforce-block-style` to rewrite every flow-style map/list into block style, regardless of how it was written:

```shell
kubesplit --input all-in-one.yml --output out --enforce-block-style
```

Input with an inline `data` map:

```yaml
data: {key1: value1, key2: value2}
```

Output with `--enforce-block-style`:

```yaml
data:
  key1: value1
  key2: value2
```

!!! note
    `--enforce-block-style` overrides `--default-flow-style` (everything ends up block style). Empty collections (`[]` and `{}`) are kept as-is, since block style has no representation for them. This option only applies in the default `rt` parsing mode.

## Line width

The maximum line width defaults to `2048` (effectively "don't wrap"). Lower it with `-w/--line-width` if you want yamkix to fold long lines:

```shell
kubesplit --input all-in-one.yml --output out --line-width 80
```

## Comment spacing

By default, end-of-line comments are left where they are. Use `-s/--spaces-before-comment` to normalize the number of spaces between content and a trailing comment:

```shell
kubesplit --input all-in-one.yml --output out --spaces-before-comment 2
```

```yaml
apiVersion: extensions/v1beta1  # exactly two spaces before the comment
```

!!! warning
    `-s` is `--spaces-before-comment` in kubesplit (an integer), **not** a "stdout" flag. Kubesplit has no `STDOUT` mode — see [Split descriptors](split-descriptors.md).

## Align end-of-line comments

Use `-a/--align-comments` to line up trailing (end-of-line) comments within each map/list to a common column:

```shell
kubesplit --input all-in-one.yml --output out --align-comments
```

Input:

```yaml
data:
  short: a # first
  a_longer_key: b # second
```

Output with `--align-comments`:

```yaml
data:
  short: a        # first
  a_longer_key: b # second
```

Comments are aligned to the widest line **within the same map or list**, so nested blocks are aligned independently. Combine it with `-s/--spaces-before-comment` to also control the gap before short comments.

## Parser mode: keep or drop comments

The parser mode is `rt` (round-trip) by default, which **preserves comments**. Switch to `-t safe/--typ safe` to drop all comments:

```shell
kubesplit --input all-in-one.yml --output out --typ safe
```

## Next steps

- See the complete option table in the [CLI options reference](../reference/cli.md).
- Read why these defaults were chosen in [How kubesplit works](../explanation/how-it-works.md).
