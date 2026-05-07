import pytest

from src.exceptions import (
    BookUnavailableError,
    EntityNotFoundError,
    UserLimitExceededError,
)
from src.models.book import BookStatus
from src.repositories.memory_repository import (
    MemoryBookRepository,
    MemoryUserRepository,
)
from src.services.library_service import LibraryService


@pytest.fixture()
def service():
    book_repo = MemoryBookRepository()
    user_repo = MemoryUserRepository()
    return LibraryService(book_repo, user_repo)


def _register_ok(service: LibraryService, name="Ivan", email="ivan@test.com") -> int:
    res = service.register_user(name, email)
    assert res["ok"] is True
    return res["user_id"]


def test_register_user_success(service: LibraryService):
    user_id = _register_ok(service, "Ivan", "ivan@test.com")
    assert user_id == 1


def test_register_user_duplicate_email(service: LibraryService):
    _register_ok(service, "Ivan", "ivan@test.com")
    res2 = service.register_user("Petro", "ivan@test.com")
    assert res2["ok"] is False


def test_issue_book_success_updates_book_and_user(service: LibraryService):
    user_id = _register_ok(service)
    book = service.add_book("Clean Code", "Robert Martin")

    msg = service.issue_book(book_id=book.id, user_id=user_id)

    assert "Clean Code" in msg
    assert book.status == BookStatus.BORROWED
    assert book.current_owner_id == user_id
    user = service.user_repo.get_by_id(user_id)
    assert user.borrowed_books_count == 1


def test_issue_book_user_not_found(service: LibraryService):
    book = service.add_book("Clean Code", "Robert Martin")
    with pytest.raises(EntityNotFoundError):
        service.issue_book(book_id=book.id, user_id=999)


def test_issue_book_book_not_found(service: LibraryService):
    user_id = _register_ok(service)
    with pytest.raises(EntityNotFoundError):
        service.issue_book(book_id=999, user_id=user_id)


def test_issue_book_book_already_borrowed(service: LibraryService):
    u1 = _register_ok(service, "Ivan", "ivan@test.com")
    u2 = _register_ok(service, "Petro", "petro@test.com")
    book = service.add_book("Clean Code", "Robert Martin")

    service.issue_book(book_id=book.id, user_id=u1)
    with pytest.raises(BookUnavailableError):
        service.issue_book(book_id=book.id, user_id=u2)


def test_issue_book_user_limit_exceeded(service: LibraryService):
    user_id = _register_ok(service)
    b1 = service.add_book("B1", "A1")
    b2 = service.add_book("B2", "A2")
    b3 = service.add_book("B3", "A3")
    b4 = service.add_book("B4", "A4")

    service.issue_book(b1.id, user_id)
    service.issue_book(b2.id, user_id)
    service.issue_book(b3.id, user_id)
    with pytest.raises(UserLimitExceededError):
        service.issue_book(b4.id, user_id)


def test_return_book_success_resets_state(service: LibraryService):
    user_id = _register_ok(service)
    book = service.add_book("Clean Code", "Robert Martin")
    service.issue_book(book.id, user_id)

    msg = service.return_book(book.id)

    assert "повернуто" in msg.lower()
    assert book.status == BookStatus.AVAILABLE
    assert book.current_owner_id is None
    user = service.user_repo.get_by_id(user_id)
    assert user.borrowed_books_count == 0


def test_return_book_when_already_available(service: LibraryService):
    book = service.add_book("Clean Code", "Robert Martin")
    msg = service.return_book(book.id)
    assert "вже" in msg.lower()


def test_find_books_by_title_or_author(service: LibraryService):
    service.add_book("Clean Code", "Robert Martin")
    service.add_book("Refactoring", "Martin Fowler")

    by_title = service.find_books("clean")
    by_author = service.find_books("fowler")

    assert len(by_title) == 1
    assert by_title[0].title == "Clean Code"
    assert len(by_author) == 1
    assert by_author[0].title == "Refactoring"
