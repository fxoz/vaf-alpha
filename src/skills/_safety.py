def validate_name(self, name: str) -> str:
    """Allow only a plain filename-like name."""
    if not isinstance(name, str) or not name:
        raise ValueError("name must be a non-empty string")

    if name in {".", ".."} or "/" in name or "\\" in name:
        raise ValueError("name must not contain path separators")

    return name
