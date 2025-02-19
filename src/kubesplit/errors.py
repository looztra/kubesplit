"""Provide the custom Kubesplit errors."""


class MissingOutputDirError(ValueError):
    """Exception raised for invalid --typ option value."""

    def __init__(self) -> None:
        """Create a new instance of InvalidTypValueError."""
        super().__init__("The following arguments are required: -o/--output-dir")


class K8SNamespaceError(ValueError):
    """Exception raised when Namespace is not set and an operation is performed on it."""

    def __init__(self) -> None:
        """Create a new instance of InvalidTypValueError."""
        super().__init__("Cannot perform requested operation on a resource without a namespace")
