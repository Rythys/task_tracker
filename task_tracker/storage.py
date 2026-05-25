"""Сохранение и загрузка данных в JSON.

Модуль работает с интерфейсом Serializable, а не с конкретными классами (DIP).
"""

import json

from task_tracker.exceptions import StorageError
from task_tracker.models.project import Project


def save_data(projects: list, filepath: str) -> None:
    """Сохранить список проектов в JSON-файл.

    Формат файла:
    {
        "projects": [
            {
                "id": "uuid",
                "name": "My Project",
                "members": [...],
                "tasks": [...]
            }
        ]
    }

    Требования:
    - Каждый проект/задача/пользователь сериализуется через to_dict()
    - При ошибке записи — StorageError
    - JSON с отступами (indent=2) для читаемости

    Args:
        projects: список объектов Project
        filepath: путь к файлу

    """

    projects_dict = [project.to_dict() for project in projects]
    data = {"projects": projects_dict}
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        raise StorageError(f"Wrong data format: {e}")

    except OSError as e:
        raise StorageError(f"Fail to save data {e}")

    except Exception as e:
        raise StorageError(f"Unknown Error: {e}")


def load_data(filepath: str) -> list:
    """Загрузить список проектов из JSON-файла.

    Требования:
    - Если файл не существует — вернуть пустой список (не ошибка) [x]
    - Для каждой задачи определить тип по полю "type" и вызвать from_dict()
    - При ошибке чтения/парсинга — StorageError

    Args:
        filepath: путь к файлу

    Returns:
        Список объектов Project
    """
    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        projects_dict = data["projects"]
        projects_list = [Project.from_dict(p) for p in projects_dict]
        for project in projects_list:
            Project.projects[project.name] = project
        return projects_list
    except FileNotFoundError:
        return []
    except (TypeError, ValueError) as e:
        raise StorageError(f"Wrong data format: {e}")

    except OSError as e:
        raise StorageError(f"Fail to save data {e}")

    except Exception as e:
        raise StorageError(f"Unknown Error: {e}")
