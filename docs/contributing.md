# How to contribute

## Prerequisites

### Mandatory

- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Optional

- [mise](https://mise.jdx.dev/)
- [Pre-Commit](https://pre-commit.com/#install)
- [shfmt](https://github.com/mvdan/sh)
- [shellcheck](https://github.com/koalaman/shellcheck)
- [editorconfig-checker](https://github.com/editorconfig-checker/editorconfig-checker)

### Install the optional prerequisites

- If you installed mise, you can simply run:

```bash
mise install
```

## Hack

- run `make setup-venv` so that `uv` inits a virtual environment with required dependencies (same as `uv sync`)

### Update the dependencies

Run `make upgrade-dependencies`, this is the same as `uv sync --upgrade`.

### Code

- run `make test` to launch unit tests
- run `make lint` to launch linters
- run `make integration-tests` to launch the integration tests

### Documentation

- run `make serve-docs` to preview the documentation locally (live reload)
- run `make build-docs` to build the static site

The documentation is written with [MkDocs](https://www.mkdocs.org/) and the
[Material](https://squidfunk.github.io/mkdocs-material/) theme, following the
[Diátaxis](https://diataxis.fr/) framework. It is published to GitHub Pages on
every push to `main`.

### Pre-Commit

- If you want to run pre-commit before each commit, run once `make precommit-install`
- If you don't want to configure a pre-commit hook (your choice, pre-commit is run by the CICD anyway), you can run it when you want, use `make precommit-run`

### Configure your editor

#### VSCode

- It's a good idea to install the [EditorConfig for VSCode extension](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig)
- Your `settings.json` (user or workspace or project) should contain:

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit",
      "source.fixAll": "explicit"
    }
  },
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "files.trimFinalNewlines": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestEnabled": true
}
```

#### Others

- Feel free to contribute any other editor configuration
