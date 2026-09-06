# Pull Request

## Description

<!-- What does this PR change and why? -->

Fixes #<issue_number>

## Changes

<!-- Bullet the key changes (code, docs, config, tests) -->

-

## How to test

<!-- Exact commands/steps a reviewer can run to verify -->

```bash
poe lint:all
poe test
make integration-tests
```

## Checklist

- [ ] PR title follows [Conventional Commits](https://www.conventionalcommits.org/) with a scope (e.g. `feat(cli): ...`)
- [ ] `poe style` run (formatting)
- [ ] `poe lint:all` passes (ruff, pylint, pyright, ty)
- [ ] `poe test` (unit tests) passes
- [ ] `make integration-tests` passes
- [ ] Docs updated under `docs/` (tutorials/how-to/reference/explanation) and registered in `mkdocs.yml`, if this changes CLI flags, behavior, or concepts
- [ ] `pre-commit run --all-files` passes
