"""Перечисления: Status, Priority, Role, допустимые переходы статусов и функции from_str."""

from enum import Enum


class Status(Enum):
    """Статусы задачи."""

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"
    CLOSED = "closed"


class Priority(Enum):
    """Приоритеты задачи (числовые значения для сортировки)."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class Role(Enum):
    """Роли пользователей."""

    DEVELOPER = "developer"
    QA = "qa"
    TEAM_LEAD = "team_lead"
    PM = "pm"


# Допустимые переходы между статусами.
# Ключ — текущий статус, значение — множество допустимых следующих статусов.
VALID_TRANSITIONS: dict[Status, set[Status]] = {
    Status.OPEN: {Status.IN_PROGRESS},
    Status.IN_PROGRESS: {Status.IN_REVIEW, Status.OPEN},
    Status.IN_REVIEW: {Status.DONE, Status.IN_PROGRESS},
    Status.DONE: {Status.CLOSED, Status.IN_PROGRESS},
    Status.CLOSED: set(),  # терминальный статус
}


def priority_to_str(priority: Priority) -> str:
    """Преобразовать приоритет в строку."""
    if priority == Priority.LOW:
        return "low"
    if priority == Priority.MEDIUM:
        return "medium"
    if priority == Priority.HIGH:
        return "high"
    if priority == Priority.CRITICAL:
        return "critical"
    return ""


def set_prority_from_str(priority_str: str) -> Priority:
    priority = None
    if priority_str == "low":
        priority = Priority.LOW
    if priority_str == "medium":
        priority = Priority.MEDIUM
    if priority_str == "high":
        priority = Priority.HIGH
    return priority


def set_status_from_str(status_str: str) -> Status:
    status = None
    if status_str == "open":
        status = Status.OPEN
    if status_str == "in_progress":
        status = Status.IN_PROGRESS
    if status_str == "in_review":
        status = Status.IN_REVIEW
    if status_str == "done":
        status = Status.DONE
    if status_str == "closed":
        status = Status.CLOSED
    return status


def set_role_from_str(role_str: str) -> Role:
    role = None
    if role_str == "developer":
        role = Role.DEVELOPER
    if role_str == "qa":
        role = Role.QA
    if role_str == "team_lead":
        role = Role.TEAM_LEAD
    if role_str == "pm":
        role = Role.PM
    return role
