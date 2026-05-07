import re


class UserRegistrationDTO:
    def __init__(self, name: str, email: str, tier: str = "regular"):
        self.name = name
        self.email = email
        self.tier = tier

    def validate(self) -> bool:
        if len(self.name) < 2:
            return False
        # Проста регулярка для перевірки пошти
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", self.email))
