from enum import Enum
from dataclasses import dataclass
from typing import Optional


class BookStatus(Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    RESERVED = "reserved"


@dataclass
class Book:
    id: int
    title: str
    author: str
    status: BookStatus = BookStatus.AVAILABLE
    current_owner_id: Optional[int] = None
