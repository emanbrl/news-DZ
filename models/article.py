from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Article:
    """Represent a normalized news article."""

    source: str
    title: str
    url: str
    category: Optional[str]
    published_at: Optional[datetime]
    description: Optional[str]