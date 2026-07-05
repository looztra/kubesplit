# File naming and layout

Information-oriented reference for how `kubesplit` names the files it generates and where it places them. For task-oriented guidance, see [Organize the output](../how-to/organize-output.md).

## File name

Each resource is written to a file named:

```text
<order-prefix><kind>--<name>.<extension>
```

- **`<order-prefix>`** — `NN--` where `NN` is the [order weight](#order-prefixes) of the resource `kind`. Empty when `-p/--no-resource-prefix` is used.
- **`<kind>`** — the resource `kind`, lower-cased (`Deployment` → `deployment`).
- **`<name>`** — `.metadata.name`, lower-cased, with any `:` replaced by `-`.
- **`<extension>`** — `yml`.

Examples:

| Kind | Name | Namespace | Generated path |
| ---- | ---- | --------- | -------------- |
| `Namespace` | `apps-demo` | — | `00--namespace--apps-demo.yml` |
| `ClusterRole` | `example-node-viewer` | — | `01--clusterrole--example-node-viewer.yml` |
| `Deployment` | `web` | `demo` | `demo/20--deployment--web.yml` |
| `Service` | `traefik-web-ui` | `ingress-controllers` | `ingress-controllers/30--service--traefik-web-ui.yml` |

## Directory layout

- **Cluster-wide resources** (no `.metadata.namespace`) are written to the **root** of the output directory.
- **Namespaced resources** are written to a **subdirectory named after their namespace** (lower-cased). The subdirectory is created if it does not exist.

Kubesplit determines the namespace solely from `.metadata.namespace` in each resource. It does not infer namespaces from a `Namespace` resource or from any `--namespace` flag used upstream.

## Order prefixes

When prefixing is enabled (the default), the `NN` weight is looked up from the resource `kind`. Applying files in lexical order therefore applies dependencies first (namespaces, then RBAC, then config/storage, then workloads, then networking). Any kind not in the table gets the fallback weight `99`.

| Weight | Kinds |
| ------ | ----- |
| `00` | `namespace` |
| `01` | `clusterrole` |
| `02` | `clusterrolebinding` |
| `03` | `serviceaccount` |
| `04` | `role` |
| `05` | `rolebinding` |
| `10` | `secret` |
| `11` | `configmap` |
| `12` | `persistentvolumeclaim` |
| `13` | `persistentvolume` |
| `20` | `deployment` |
| `21` | `daemonset` |
| `22` | `statefulset` |
| `23` | `job` |
| `24` | `cronjob` |
| `25` | `replicaset` |
| `30` | `service` |
| `31` | `ingress` |
| `40` | `networkpolicy` |
| `41` | `poddisruptionbudget` |
| `42` | `priorityclass` |
| `99` | any other (unknown) kind |

## Lists

A document whose `kind` ends with `List` (for example `ConfigMapList`, `RoleList`) is written as a **single file** and is **not** exploded into its individual items. The file name follows the usual scheme, with the fallback weight `99` and a synthetic name `list_<n>` (the 0-based index of the list within the input):

```text
99--configmaplist--list_0.yml
99--rolelist--list_1.yml
```

Lists are treated as cluster-wide, so they are written to the root of the output directory.
