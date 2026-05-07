from dataclasses import dataclass, field


@dataclass
class User:
    id: int
    name: str
    email: str
    borrowed_books_count: int = field(default=0)
