from __future__ import annotations

from typing import Dict, List, Optional

from src.models.book import Book
from src.models.user import User


class MemoryBookRepository:
    def __init__(self) -> None:
        self.books: Dict[int, Book] = {}

    def save(self, book: Book) -> None:
        self.books[book.id] = book

    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self.books.get(book_id)

    def search_by_query(self, query: str) -> List[Book]:
        q = (query or "").lower()
        return [
            b
            for b in self.books.values()
            if q in b.title.lower() or q in b.author.lower()
        ]


class MemoryUserRepository:
    def __init__(self) -> None:
        self.users: Dict[int, User] = {}

    def save(self, user: User) -> None:
        self.users[user.id] = user

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        return next((u for u in self.users.values() if u.email == email), None)
