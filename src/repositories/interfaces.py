from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.book import Book
from src.models.user import User


class IUserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None: pass
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]: pass
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]: pass


class IBookRepository(ABC):
    @abstractmethod
    def save(self, book: Book) -> None: pass
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]: pass
    @abstractmethod
    def search_by_query(self, query: str) -> List[Book]: pass
