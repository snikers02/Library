from __future__ import annotations

from typing import Dict, List, Optional

from src.exceptions import (
    BookUnavailableError,
    EntityNotFoundError,
    UserLimitExceededError,
)
from src.models.book import Book, BookStatus
from src.models.user import User


class LibraryService:
    """
    Сервісний шар: вся бізнес-логіка бібліотеки.

    Залежить від репозиторіїв (book_repo/user_repo), а не від способу зберігання даних.
    """

    MAX_BOOKS_PER_USER = 3

    def __init__(self, book_repo, user_repo) -> None:
        self.book_repo = book_repo
        self.user_repo = user_repo
        self._next_user_id = 1
        self._next_book_id = 1

    def _get_user_or_raise(self, user_id: int) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise EntityNotFoundError("Книгу або користувача не знайдено")
        return user

    def _get_book_or_raise(self, book_id: int) -> Book:
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise EntityNotFoundError("Книгу або користувача не знайдено")
        return book

    def register_user(self, name: str, email: str) -> Dict[str, object]:
        if not name or not email:
            return {"ok": False, "message": "name/email required"}

        if self.user_repo.get_by_email(email):
            return {"ok": False, "message": "email already exists"}

        user = User(self._next_user_id, name, email)
        self._next_user_id += 1
        self.user_repo.save(user)
        return {"ok": True, "user_id": user.id}

    def add_book(self, title: str, author: str) -> Optional[Book]:
        if not title or not author:
            return None
        book = Book(self._next_book_id, title, author)
        self._next_book_id += 1
        self.book_repo.save(book)
        return book

    def find_books(self, query: str) -> List[Book]:
        return self.book_repo.search_by_query(query)

    def issue_book(self, book_id: int, user_id: int) -> str:
        """Сценарій видачі книги з декількома перевірками"""
        book = self._get_book_or_raise(book_id)
        user = self._get_user_or_raise(user_id)

        if book.status != BookStatus.AVAILABLE:
            raise BookUnavailableError(f"Книга '{book.title}' вже видана іншому читачу")

        if user.borrowed_books_count >= self.MAX_BOOKS_PER_USER:
            raise UserLimitExceededError(
                f"Користувач {user.name} вже має {self.MAX_BOOKS_PER_USER} книги"
            )

        book.status = BookStatus.BORROWED
        book.current_owner_id = user.id
        user.borrowed_books_count += 1

        return f"Книгу '{book.title}' видано користувачу {user.name}"

    def return_book(self, book_id: int) -> str:
        """Сценарій повернення книги"""
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise EntityNotFoundError("Книгу не знайдено")

        if book.status == BookStatus.AVAILABLE:
            return "Книга вже є в бібліотеці"

        user = self.user_repo.get_by_id(book.current_owner_id)
        if user:
            user.borrowed_books_count -= 1

        book.status = BookStatus.AVAILABLE
        book.current_owner_id = None
        return f"Книгу '{book.title}' успішно повернуто"
