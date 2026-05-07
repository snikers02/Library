from __future__ import annotations

from src.dto.requests import UserRegistrationDTO
from src.exceptions import LibraryError
from src.services.library_service import LibraryService


class LibraryController:
    def __init__(self, library_service: LibraryService):
        self.library_service = library_service

    def _ok(self, payload: dict) -> dict:
        return {"status": "success", **payload}

    def _err(self, message: str, *, status: str = "business_error") -> dict:
        return {"status": status, "message": message}

    def register_user(self, dto: UserRegistrationDTO):
        if not dto.validate():
            return self._err("Невалідні дані користувача або email.", status="error")

        res = self.library_service.register_user(dto.name, dto.email)
        if not res.get("ok"):
            return self._err(str(res.get("message", "Помилка")), status="error")
        return self._ok({"user_id": res["user_id"]})

    def borrow_book(self, user_id: int, book_id: int):
        try:
            msg = self.library_service.issue_book(book_id=book_id, user_id=user_id)
            return self._ok({"message": msg})
        except (LibraryError, ValueError) as e:
            return self._err(str(e))

    def return_book(self, book_id: int):
        try:
            msg = self.library_service.return_book(book_id)
            return self._ok({"message": msg})
        except (LibraryError, ValueError) as e:
            return self._err(str(e))

    def search_books(self, query: str):
        books = self.library_service.find_books(query)
        return self._ok({
            "count": len(books),
            "items": [
                {
                    "id": b.id,
                    "title": b.title,
                    "author": b.author,
                    "status": b.status.value,
                }
                for b in books
            ],
        })
