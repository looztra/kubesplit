# Install kubesplit

`Kubesplit` is published on [pypi.org](https://pypi.org/project/kubesplit/) and as a Docker image. Pick the method that fits your workflow.

## With uv (recommended)

[uv](https://docs.astral.sh/uv/guides/tools/) installs `kubesplit` as an isolated standalone tool:

```shell
uv tool install kubesplit
kubesplit --version
```

Run it once without installing:

```shell
uvx kubesplit --input all-in-one.yml --output out
```

## With pip

```shell
pip3 install -U --user kubesplit
kubesplit --input all-in-one.yml --output out
```

## With mise

[mise](https://mise.jdx.dev/) can manage `kubesplit` (and pin its version) through its [pipx backend](https://mise.jdx.dev/dev-tools/backends/pipx.html), which relies on `uv` when available:

```toml title="Sample mise.toml"
[tools]
"pipx:kubesplit" = "0.5.0"
uv = "0.8.9"
```

Then:

```shell
mise install
```

## With Docker

Use the published image when you don't want to install anything locally. Mount your working directory so kubesplit can read the input and write the output:

```shell
# Use latest
docker image pull looztra/kubesplit

# Split a file mounted from the current directory
docker container run -ti --rm \
  -v "$(pwd):/code" -w /code \
  looztra/kubesplit \
  --input all-in-one.yml \
  --output out
```

Read from `STDIN` instead of a file:

```shell
cat all-in-one.yml | docker container run -i --rm \
  -v "$(pwd):/code" -w /code \
  looztra/kubesplit \
  --output out
```

Available tags are listed on [Docker Hub](https://hub.docker.com/r/looztra/kubesplit/tags).

## Next steps

- Split your first file in the [Getting started tutorial](../tutorials/getting-started.md).
- See every input/output option in [Split descriptors](split-descriptors.md).
