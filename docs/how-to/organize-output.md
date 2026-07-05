# Organize the output

`Kubesplit` names each generated file after the resource it contains and groups files by namespace. This guide shows how to control that layout. For the exhaustive rules, see [File naming and layout](../reference/file-naming.md).

## Default layout: prefixed and grouped by namespace

By default every file is named:

```text
<order-prefix>--<kind>--<name>.yml
```

Cluster-wide resources (`Namespace`, `ClusterRole`, `ClusterRoleBinding`, …) go to the **root** of the output directory; namespaced resources go into a **subdirectory named after their namespace**.

```shell
kubesplit --input test-assets/source/all-in-one.yml \
          --output out \
          --no-quotes-preserved \
          --clean-output-dir
```

```text
out
├── apps-demo
│   └── 05--rolebinding--example-ns-demo-developer-binding.yml
├── apps-integration
│   └── 05--rolebinding--example-ns-integration-developer-binding.yml
├── ingress-controllers
│   ├── 03--serviceaccount--traefik-ingress-controller.yml
│   ├── 11--configmap--traefik-conf.yml
│   ├── 12--persistentvolumeclaim--traefik-acme.yml
│   ├── 20--deployment--traefik-ingress-controller.yml
│   ├── 30--service--traefik-ingress-endpoint.yml
│   ├── 30--service--traefik-web-ui.yml
│   └── 31--ingress--traefik-web-ui.yml
├── 00--namespace--apps-demo.yml
├── 00--namespace--apps-integration.yml
├── 00--namespace--ingress-controllers.yml
├── 01--clusterrole--example-node-viewer.yml
├── 01--clusterrole--example-traefik-ingress-controller.yml
├── 02--clusterrolebinding--example-node-viewer-developer.yml
└── 02--clusterrolebinding--example-traefik-ingress-controller.yml

3 directories, 16 files
```

## Why the number prefixes?

The `00`, `01`, `20`, `30`… prefixes are **apply-order weights** derived from the resource `kind`. Namespaces come first (`00`), RBAC next (`01`–`05`), config and storage in the middle (`10`–`13`), workloads (`20`–`25`), then networking (`30`–`42`). Applying the files in lexical order (which is what `kubectl apply -f out/ --recursive` does) therefore respects the usual dependency order.

The full prefix table lives in [File naming and layout](../reference/file-naming.md#order-prefixes).

## Drop the prefixes with `--no-resource-prefix`

If you don't need an apply order (for example when files feed a GitOps tool that resolves ordering itself), use `-p/--no-resource-prefix`:

```shell
kubesplit --input test-assets/source/all-in-one.yml \
          --output out \
          --no-quotes-preserved \
          --no-resource-prefix \
          --clean-output-dir
```

```text
out
├── apps-demo
│   └── rolebinding--example-ns-demo-developer-binding.yml
├── ingress-controllers
│   ├── configmap--traefik-conf.yml
│   ├── deployment--traefik-ingress-controller.yml
│   ├── ingress--traefik-web-ui.yml
│   ├── persistentvolumeclaim--traefik-acme.yml
│   ├── serviceaccount--traefik-ingress-controller.yml
│   ├── service--traefik-ingress-endpoint.yml
│   └── service--traefik-web-ui.yml
├── clusterrole--example-node-viewer.yml
├── clusterrolebinding--example-node-viewer-developer.yml
└── namespace--apps-demo.yml

...
```

The namespace grouping is unaffected — only the `NN--` prefix is removed.

## Next steps

- See the complete naming rules and prefix table in [File naming and layout](../reference/file-naming.md).
- Understand how kubesplit decides a resource's namespace in [How kubesplit works](../explanation/how-it-works.md).
