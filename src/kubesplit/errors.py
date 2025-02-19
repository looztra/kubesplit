"""Provide the custom Kubesplit errors."""


class MissingOutputDirError(ValueError):
    """Exception raised for invalid --typ option value."""

    def __init__(self) -> None:
        """Create a new instance of InvalidTypValueError."""
        super().__init__("The following arguments are required: -o/--output-dir")
