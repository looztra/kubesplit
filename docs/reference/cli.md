# CLI options

Information-oriented reference for the `kubesplit` command line. For guided examples, see the [how-to guides](../how-to/split-descriptors.md).

## Synopsis

```text
kubesplit [OPTIONS]
```

`kubesplit` takes no positional arguments: the input is a single file or `STDIN`, and the output is always a directory (`-o/--output`).

## Options

| Option | Short | Type | Default | Description |
| ------ | ----- | ---- | ------- | ----------- |
| `--input` | `-i` | TEXT | `None` (STDIN) | the file to parse, or `STDIN` if not specified or if the value is `-`. |
| `--output-dir` / `--output` | `-o` | TEXT | — (**required**) | the output target directory. Created if it does not exist. |
| `--clean-output-dir` | `-c` | flag | off | clean the output directory (`rmtree`) before writing. |
| `--no-resource-prefix` | `-p` | flag | off | by default resource files are number-prefixed; this flag disables the prefix. |
| `--typ` | `-t` | `safe`\|`rt` | `rt` | the yaml parser mode. `safe` removes all comments. |
| `--no-explicit-start` | `-n` | flag | off | explicit start (`---`) is on by default; this disables it. |
| `--explicit-end` | `-e` | flag | off | explicit end (`...`) is off by default; this enables it. |
| `--no-quotes-preserved` | `-q` | flag | off | quotes are preserved by default; this removes unnecessary ones. |
| `--enforce-double-quotes` | `-E` | flag | off | when `--no-quotes-preserved` is set, re-quote with double quotes instead of single. |
| `--default-flow-style` | `-f` | flag | off | enable the default (JSON-like) flow style. |
| `--enforce-block-style` | `-B` | flag | off | convert flow-style (JSON-like) maps and lists to block style. Overrides `--default-flow-style`. Empty collections (`[]`/`{}`) are kept as-is. |
| `--align-comments` | `-a` | flag | off | align EOL comments within each dict/list to the maximum column. |
| `--no-dash-inwards` | `-d` | flag | off | dashes are pushed inwards by default; this keeps them at the sequence level. |
| `--spaces-before-comment` | `-s` | INTEGER | `None` | number of spaces between content and a trailing comment. If unset, comments are left as is. |
| `--line-width` | `-w` | INTEGER | `2048` | maximum line width. |
| `--version` | `-v` | flag | | show the kubesplit version (and the embedded yamkix version). |
| `--help` | `-h` | flag | | show the help message and exit. |

## Defaults summary

Running `kubesplit -o out` (the only required option) applies:

- `parsing_mode = rt` (comments preserved)
- `explicit_start = True` (`---` added)
- `explicit_end = False`
- `default_flow_style = False`
- `enforce_block_style = False`
- `align_comments = False`
- `dash_inwards = True`
- `quotes_preserved = True`
- `enforce_double_quotes = False`
- `spaces_before_comment = None` (comments left as is)
- `line_width = 2048`
- `prefix_resource_files = True` (files are `NN--` prefixed)
- `clean_output_dir = False` (existing files are left in place)
- input `STDIN`

## `--help` output

```text
 Usage: kubesplit [OPTIONS]

 Split a set of Kubernetes descriptors to a set of files.

 The yaml format of the generated files can be tuned using the same
 parameters as yamkix. By default, explicit_start is 'On', explicit_end
 is 'Off' and array elements are pushed inwards. Comments are preserved
 thanks to default parsing mode 'rt'.

╭─ Options ────────────────────────────────────────────────────────────╮
│ --input                  -i      TEXT       the file to parse, or     │
│                                             STDIN if not specified    │
│                                             or if value is -          │
│ --output-dir,--output    -o      TEXT       the name of the output    │
│                                             target directory.         │
│ --clean-output-dir       -c                 clean the output          │
│                                             directory (rmtree).       │
│ --no-resource-prefix     -p                 disable the number        │
│                                             prefix on resource files. │
│ --typ                    -t      [safe|rt]  the yaml parser mode.     │
│                                             [default: rt]             │
│ --no-explicit-start      -n                 disable explicit start.   │
│ --explicit-end           -e                 enable explicit end.      │
│ --no-quotes-preserved    -q                 don't preserve quotes.    │
│ --enforce-double-quotes  -E                 enforce double quotes     │
│                                             with -q.                  │
│ --default-flow-style     -f                 enable the default flow   │
│                                             style.                    │
│ --enforce-block-style    -B                 convert flow-style to     │
│                                             block style.             │
│ --align-comments         -a                 align EOL comments to     │
│                                             max column.              │
│ --no-dash-inwards        -d                 dash at sequence level.   │
│ --spaces-before-comment  -s      INTEGER    spaces between comments   │
│                                             and content.              │
│ --line-width             -w      INTEGER    maximum line width.       │
│                                             [default: 2048]           │
│ --version                -v                 show kubesplit version.   │
│ --help                   -h                 Show this message and     │
│                                             exit.                     │
╰──────────────────────────────────────────────────────────────────────╯
```

Run `kubesplit --help` locally for the authoritative, full-width output.
