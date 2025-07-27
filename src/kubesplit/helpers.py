"""Provide generic helpers."""

from yamkix import __version__ as yamkix_version

from kubesplit import __version__


def get_version_string() -> str:
    """Return the version string."""
    return "kubesplit v" + __version__ + " (yamkix v" + yamkix_version + ")"


def print_version() -> None:
    """Print version."""
    print(get_version_string())  # noqa: T201
