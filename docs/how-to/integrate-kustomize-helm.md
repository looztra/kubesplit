# Use with Kustomize and Helm

`Kubesplit` reads from `STDIN`, so it drops straight into a pipeline behind any tool that renders a multidoc Kubernetes stream — most commonly `kustomize` and `helm`. This turns a single opaque render into a reviewable tree of one-resource-per-file.

Pass `-` (or nothing) as the input and let kubesplit read the piped stream; give it an output directory with `-o/--output`.

## With Kustomize

```shell
kustomize build overlays/prod | kubesplit --no-quotes-preserved --input - --output generated/prod
```

Or with `kubectl`'s built-in kustomize:

```shell
kubectl kustomize overlays/prod | kubesplit -q -i - -o generated/prod
```

## With Helm

```shell
helm template my-release my-chart \
  --namespace target-ns \
  --values config.yml \
| kubesplit --no-quotes-preserved --input - --output generated/prod
```

## Keep the output directory in sync

When you re-render after a change, add `-c/--clean-output-dir` so that files for removed resources don't linger:

```shell
kustomize build overlays/prod | kubesplit -q -c -i - -o generated/prod
```

!!! warning
    `--clean-output-dir` recursively deletes the output directory before writing. Point it only at a directory dedicated to generated output.

## Next steps

- Tune the emitted YAML in [Tune the YAML formatting](tune-yaml-formatting.md).
- Understand the resource detection and ordering in [How kubesplit works](../explanation/how-it-works.md).
- Read why teams split their renders (reviewable diffs, apply order, consistent formatting) in [Ecosystem](../explanation/ecosystem.md).
