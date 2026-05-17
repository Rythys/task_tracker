"""Абстрактный базовый класс задачи Task."""

import uuid
from abc import abstractmethod
from datetime import datetime

from task_tracker import global_states
from task_tracker.enums import VALID_TRANSITIONS, Priority, Status, priority_to_str
from task_tracker.exceptions import InvalidStatusTransitionError, ValidationError
from task_tracker.interfaces import Displayable, Serializable
from task_tracker.mixins import HistoryMixin, TimestampMixin


class Task(
    Serializable, Displayable, TimestampMixin, HistoryMixin
):  # убрал ABC, так как абстрактные методы уже есть
    """Абстрактный базовый класс задачи.

    Поля:
        id (str): уникальный идентификатор (UUID4)
        title (str): название задачи (3–128 символов, через property)
        description (str): описание задачи
        _status (Status): текущий статус (защищённое поле)
        priority (Priority): приоритет
        assignee (User | None): исполнитель
        created_at (datetime): дата создания
        updated_at (datetime): дата последнего изменения

    Абстрактные методы (реализуются в наследниках):
        estimate() -> float: оценка трудоёмкости в часах
        label() -> str: строковая метка типа ([BUG], [FEATURE], [EPIC])

    Магические методы (нужно реализовать):
        __str__: [LABEL] #id_short — title (PRIORITY)
        __repr__: ClassName(id='...', title='...', status=STATUS)
        __eq__, __hash__: сравнение и хеширование по id
        __lt__, __le__, __gt__, __ge__: сравнение по priority (для сортировки)

    Инкапсуляция:
        - status доступен только на чтение (через @property)
        - изменение статуса — только через change_status()
        - title валидируется через property setter (3–128 символов)
    """

    def __init__(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
    ):
        super().__init__()
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self._status = Status.OPEN
        self.priority = priority
        self.assignee = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    # ── title property ──────────────────────────────────────────────

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        # TODO: Добавьте валидацию длины (3–128 символов).
        # При невалидном значении выбрасывайте ValidationError.
        if len(value) < 3 or len(value) > 128:
            raise ValidationError("Title length must be in range 3-128!")
        self._title = value

    # ── status property ─────────────────────────────────────────────

    @property
    def status(self) -> Status:
        return self._status

    def change_status(self, new_status: Status) -> None:
        """Изменить статус задачи с проверкой допустимости перехода.

        Допустимые переходы определены в enums.VALID_TRANSITIONS.
        При недопустимом переходе — InvalidStatusTransitionError.
        При изменении — обновить updated_at и записать в историю (HistoryMixin).

        Args:
            new_status: новый статус
        """
        allowed_transitions = VALID_TRANSITIONS.get(self._status, [])

        if new_status not in allowed_transitions:
            raise InvalidStatusTransitionError(
                f"Переход из {self._status.value} в {new_status.value} невозможен!"
            )

        old_status = self._status.value
        self._status = new_status
        self.updated_at = datetime.now()

        self._record_transition(old_status, new_status.value)

    # ── абстрактные методы ──────────────────────────────────────────

    @abstractmethod
    def estimate(self) -> float:
        """Оценка трудоёмкости в часах. Зависит от типа задачи."""
        ...

    @abstractmethod
    def label(self) -> str:
        """Строковая метка типа задачи: [BUG], [FEATURE], [EPIC]."""
        ...

    # ── Serializable ────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Сериализовать задачу в словарь.

        Должен включать поле "type" ("bug", "feature", "epic"),
        assignee_id вместо объекта User, даты в ISO 8601.
        """

        return {
            "type": self.label().strip("[]").lower(),
            "id": self.id,
            "title": self._title,
            "description": self.description,
            "status": self._status.value,
            "priority": self.priority.value,
            "assignee_id": self.assignee.id if self.assignee else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "history": self.history,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Создать задачу из словаря. Выбор класса по полю 'type'."""
        task = cls(data["title"])
        task.description = data.get("description", "")
        task.priority = Priority(data.get("priority", Priority.MEDIUM))
        task.id = data["id"]
        task._status = Status(data["status"])
        task.assignee = (
            global_states.users_by_id.get(data["assignee_id"]) if data.get("assignee_id") else None
        )
        task.created_at = datetime.fromisoformat(data["created_at"])
        task.updated_at = datetime.fromisoformat(data["updated_at"])
        task._history = data.get("history", [])
        return task

    # ── Displayable ─────────────────────────────────────────────────

    def short_display(self) -> str:
        """Краткое представление: [LABEL] title — PRIORITY — STATUS"""
        return (
        f"{self.label()} {self.title} - "
        f"{priority_to_str(self.priority)} - {self.status.value}"
    )

    def full_display(self) -> str:
        """Полное представление со всеми полями."""
        disp_str = f"id:          {self.id}\n\
title:       {self._title}\n\
description: {self.description}\n\
status:      {self._status.value}\n\
priority:    {self.priority.value}\n\
assignee:    {self.assignee}\n\
created_at:  {self.created_at}\n\
updated_at:  {self.updated_at}"

        return disp_str

    # ── Магические методы (TODO: реализовать) ───────────────────────
    # __str__:  [BUG] #abc12 — Fix login (HIGH)
    # __repr__: Bug(id='abc12', title='Fix login', status=OPEN)
    # __eq__, __hash__: по id
    # __lt__, __le__, __gt__, __ge__: по priority.value

    def __str__(self) -> str:
        return f"{self.label()} #{self.id} — {self.title} ({self.priority})"

    def __repr__(self) -> str:
        return (
        f"{self.__class__.__name__}("
        f"id='{self.id}', "
        f"title='{self.title}', "
        f"status='{self.status.value}'"  # Лучше использовать .value для статуса
        f")"
    )

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        if not isinstance(other, Task):
            return False
        return self.priority.value < other.priority.value

    def __le__(self, other):
        if not isinstance(other, Task):
            return False
        return self.priority.value <= other.priority.value

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other
