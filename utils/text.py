import re


def normalize_description(text):
    """Normalize whitespace and location prefixes in an article description."""

    if not text:
        return None

    text = re.sub(r"\s+", " ", text).strip()

    text = re.sub(
        r"^(ALGIERS|NEW YORK)\s*-\s*",
        r"\1 - ",
        text,
    )

    return text