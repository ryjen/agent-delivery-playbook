def normalize_tag(value: str) -> str:
    """Normalize a display tag for stable identifiers."""
    return value.strip().lower().replace(" ", "-")
