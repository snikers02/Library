class LibraryError(Exception):
    """Базовий клас для всіх помилок бібліотеки"""
    pass


class BookUnavailableError(LibraryError):
    """Викидається, якщо книга вже зайнята"""
    pass


class UserLimitExceededError(LibraryError):
    """Викидається, якщо користувач хоче взяти більше ніж 3 книги"""
    pass


class EntityNotFoundError(LibraryError):
    """Викидається, якщо книгу або користувача не знайдено"""
    pass
