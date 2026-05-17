"""Конкретные типы задач: Bug, Feature, Epic."""

from task_tracker.enums import Priority
from task_tracker.models.base import Task
from task_tracker.validators import RangeValidator


class Bug(Task):
    """Баг-репорт.

    Дополнительные поля:
        severity (int): критичность от 1 до 10 (через RangeValidator)
        steps_to_reproduce (str): шаги воспроизведения

    Оценка трудоёмкости: severity * 2 часов
    Метка: [BUG]
    """

    severity = RangeValidator(min_value=1, max_value=10)

    def __init__(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        severity: int = 1,
        steps_to_reproduce: str = "",
    ):
        super().__init__(title, description, priority)
        self.severity = severity
        self.steps_to_reproduce = steps_to_reproduce

    def estimate(self) -> float:
        """Оценка: severity * 2 часов."""
        return self.severity * 2

    def label(self) -> str:
        """Метка: [BUG]"""
        return f"[{self.__class__.__name__.upper()}]"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["severity"] = self.severity
        data["steps_to_reproduce"] = self.steps_to_reproduce
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Bug":
        bug = super().from_dict(data)

        bug.severity = data.get("severity")
        bug.steps_to_reproduce = data.get("steps_to_reproduce")

        return bug


class Feature(Task):
    """Запрос на новую функциональность.

    Дополнительные поля:
        business_value (int): бизнес-ценность от 1 до 10 (через RangeValidator)
        complexity (int): техническая сложность от 1 до 10 (через RangeValidator)

    Оценка трудоёмкости: (business_value + complexity) * 1.5 часов
    Метка: [FEATURE]
    """

    business_value = RangeValidator(min_value=1, max_value=10)
    complexity = RangeValidator(min_value=1, max_value=10)

    def __init__(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        business_value: int = 5,
        complexity: int = 5,
    ):
        super().__init__(title, description, priority)
        self.business_value = business_value
        self.complexity = complexity

    def estimate(self) -> float:
        """Оценка: (business_value + complexity) * 1.5 часов."""
        return (self.business_value + self.complexity) * 1.5

    def label(self) -> str:
        """Метка: [FEATURE]"""
        return f"[{self.__class__.__name__.upper()}]"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["business_value"] = self.business_value
        data["complexity"] = self.complexity
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Feature":
        feature = super().from_dict(data)

        feature.business_value = data.get("business_value")
        feature.complexity = data.get("complexity")

        return feature


class Epic(Task):
    """Эпик — крупная задача, содержащая подзадачи.

    Дополнительные поля:
        subtasks (list[Task]): список подзадач (Bug или Feature)

    Оценка трудоёмкости: сумма estimate() всех подзадач × 1.2
    Метка: [EPIC]
    """

    def __init__(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        subtasks: list | None = None,
    ):
        super().__init__(title, description, priority)
        self.subtasks = subtasks if subtasks is not None else []

    def estimate(self) -> float:
        """Оценка: сумма estimate() подзадач × 1.2 (коэффициент координации)."""
        return sum(task.estimate() for task in self.subtasks) * 1.2

    def label(self) -> str:
        """Метка: [EPIC]"""
        return f"[{self.__class__.__name__.upper()}]"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["subtasks"] = []
        for subtask in self.subtasks:
            data["subtasks"].append(subtask.to_dict())
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Epic":
        epic = super().from_dict(data)
        epic.subtasks = []

        subtasks_list = [t for t in data.get("subtasks", [])]
        for subtask in subtasks_list:
            if subtask["type"] == "bug":
                epic.subtasks.append(Bug.from_dict(subtask))
            if subtask["type"] == "feature":
                epic.subtasks.append(Feature.from_dict(subtask))
            if subtask["type"] == "epic":
                epic.subtasks.append(Epic.from_dict(subtask))
        return epic
