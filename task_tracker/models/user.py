"""Модель пользователя."""

import uuid

from task_tracker.enums import Role
from task_tracker.interfaces import Displayable, Serializable
from task_tracker.validators import StringLengthValidator


class User(Serializable, Displayable):
    """Пользователь (участник проекта).

    Поля:
        id (str): уникальный идентификатор (UUID4)
        name (str): имя пользователя (2–64 символа, через StringLengthValidator)
        role (Role): роль в команде

    Магические методы (TODO):
        __str__: имя (роль)
        __repr__: User(id='...', name='...', role=ROLE)
        __eq__, __hash__: по id
    """

    users = dict()
    users_by_id = dict()

    name = StringLengthValidator(min_length=2, max_length=64)

    def __init__(self, name: str, role: Role = Role.DEVELOPER):
        self.id = str(uuid.uuid4())
        self.name = name
        self.role = role

        User.users[self.name] = self
        User.users_by_id[self.id] = self

    # ── Serializable ────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Сериализовать пользователя в словарь."""
        return {"id": self.id, "name": self.name, "role": self.role.value}

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Создать пользователя из словаря."""
        user = cls(data["name"], Role(data.get("role", Role.DEVELOPER)))
        user.id = data["id"]
        return user

    # ── Displayable ─────────────────────────────────────────────────

    def short_display(self) -> str:
        return f"name = {self.name}, role = {self.role.value}"

    def full_display(self) -> str:
        return f"id = {self.id}, name = {self.name}, role = {self.role.value}"

    # ── Magic ─────────────────────────────────────────────────

    def __str__(self) -> str:
        return f"{self.name} ({self.role})"

    def __repr__(self) -> str:
        return f"User(id='{self.id}', name='{self.name}', role='{self.role}')"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
