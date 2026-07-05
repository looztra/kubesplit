# Control quotes

`Kubesplit` reformats every resource it writes using [yamkix](https://github.com/looztra/yamkix), so it inherits yamkix's quote-handling options. This guide shows the before/after behavior.

## Preserve quotes (default)

By default, quotes present in the input are kept exactly as they were — same characters, same quote type (single or double).

Given this input:

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
    number_no_quotes: 1
    number_single_quotes: '1'
```

the generated file is identical (comments preserved, quotes untouched):

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
    number_no_quotes: 1
    number_single_quotes: '1'
```

## Remove unnecessary quotes with `-q/--no-quotes-preserved`

Use `-q/--no-quotes-preserved` to strip quotes that are not required:

```shell
kubesplit --input replicaset.yml --output out --no-quotes-preserved
```

With this flag:

- Quotes around **pure strings** are removed.
- Quotes around **booleans and numbers** are kept but normalized to single quotes (so YAML still reads them as strings where you meant strings).
- Values that had no quotes stay unquoted.

The annotations above become:

```yaml
    string_no_quotes: frontend
    string_single_quotes: frontend
    string_double_quotes: frontend
    boolean_no_quotes: true
    boolean_single_quotes: 'true'
    number_no_quotes: 1
    number_single_quotes: '1'
```

!!! note
    `kubesplit` is not fully Kubernetes-aware: `--no-quotes-preserved` applies to the whole document, not only to string-sensitive fields such as `.metadata.annotations` or container environment values. Review the result if you rely on quoting to keep specific values as strings.

## Force double quotes with `-E/--enforce-double-quotes`

When you strip quotes with `-q`, kubesplit re-quotes booleans/numbers with **single** quotes by default. Add `-E/--enforce-double-quotes` to use **double** quotes instead:

```shell
kubesplit --input replicaset.yml --output out --no-quotes-preserved --enforce-double-quotes
```

```yaml
    boolean_single_quotes: "true"
    number_single_quotes: "1"
```

`-E` has no effect without `-q` (there is nothing to re-quote when quotes are preserved).

## Next steps

- Adjust other aspects of the emitted YAML in [Tune the YAML formatting](tune-yaml-formatting.md).
- Read the reasoning behind quote handling in [How kubesplit works](../explanation/how-it-works.md).
