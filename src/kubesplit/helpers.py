"""Provide generic helpers."""

from kubesplit import __version__


def get_version_string() -> str:
    """Return the version string."""
    return "kubesplit v" + __version__


def print_version() -> None:
    """Print version."""
    print(get_version_string())  # noqa: T201
