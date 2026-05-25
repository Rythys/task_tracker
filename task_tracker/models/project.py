"""Модель проекта."""

import uuid

from task_tracker.interfaces import Displayable, Serializable
from task_tracker.models.tasks import Bug, Epic, Feature
from task_tracker.models.user import User
from task_tracker.validators import StringLengthValidator


class Project(Serializable, Displayable):
    """Проект, содержащий задачи и участников (композиция).

    Поля:
        id (str): уникальный идентификатор (UUID4)
        name (str): название проекта (3–128 символов)
        tasks (list[Task]): список задач
        members (list[User]): участники проекта

    Магические методы (TODO: реализовать):
        __len__: количество задач
        __contains__: проверка наличия задачи по id (строка)
        __iter__: итерация по задачам
        __getitem__: получение задачи по индексу или срезу
        __str__: название проекта (N задач, M участников)
        __repr__: Project(id='...', name='...')
    """
    projects = dict()

    name = StringLengthValidator(min_length=3, max_length=128)

    def __init__(self, name: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.tasks: list = []
        self.members: list = []

        Project.projects[self.name] = self

    # ── Serializable ────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "members": [member.to_dict() for member in self.members],
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        project = cls(name=data["name"])
        project.id = data["id"]

        project.members = [User.from_dict(m) for m in data.get("members", [])]

        for task in data.get("tasks", []):
            if task["type"] == "bug":
                project.tasks.append(Bug.from_dict(task))
            if task["type"] == "feature":
                project.tasks.append(Feature.from_dict(task))
            if task["type"] == "epic":
                project.tasks.append(Epic.from_dict(task))

        return project

    # ── Displayable ─────────────────────────────────────────────────

    def short_display(self) -> str:
        return f"Project: name = {self.name},\n tasks = {self.tasks}\n"

    def full_display(self) -> str:
        disp_str = f"{self.id}\n\
        {self.name}\n\
        {self.tasks}\n\
        {self.members}\n"
        return disp_str

    # ── Магические методы (TODO: реализовать) ───────────────────────
    # __len__: len(self.tasks)
    # __contains__: task_id (str) in project → True/False
    # __iter__: iter(self.tasks)
    # __getitem__: self.tasks[index] или self.tasks[slice]

    def __len__(self) -> str:
        return len(self.tasks)

    def __contains__(self, task_id: str) -> bool:
        return any(filter(lambda x: x.id == task_id, self.tasks))

    def __iter__(self):
        return iter(self.tasks)

    def __getitem__(self, index: int):
        return self.tasks[index]
