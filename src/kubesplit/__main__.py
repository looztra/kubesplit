"""Allow kubesplit to be executable through `python -m kubesplit`."""

from kubesplit._cli import app

if __name__ == "__main__":  # pragma: no cover
    app()
