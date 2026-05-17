from task_tracker import global_states
from task_tracker.cli_menu.task_menu import make_subtask
from task_tracker.cli_menu.user_menu import make_user
from task_tracker.models.project import Project


def make_project():
    project_name = input("Введите название проекта: ")
    new_project = Project(name=project_name)

    default_is_subtasks = "n"
    is_subtasks = "y"
    while is_subtasks == "y":
        user_input = input("Добавить подзадачу? [y/n]: ")
        is_subtasks = user_input if user_input else default_is_subtasks
        if is_subtasks != "y":
            break
        task_title, task = make_subtask()
        new_project.tasks.append(task)

    default_is_members = "n"
    is_members = "y"
    while is_members == "y":
        user_input = input("Добавить участника? [y/n]: ")
        is_members = user_input if user_input else default_is_members
        if is_members != "y":
            break
        member = make_user()
        new_project.members.append(member)
    global_states.projects[project_name] = new_project
    from task_tracker.cli import projects_menu

    return projects_menu


def delete_project():
    project_name = input("Введите название проекта: ")
    print(global_states.projects.pop(project_name, "Проектов с таким названием нет"))
    from task_tracker.cli import projects_menu

    return projects_menu


def project_report():
    project_name = input("Введите название проекта: ")
    project = global_states.projects[project_name]
    print(f"=== Сводка: {project_name} ===\nВсего задач: {len(project)}\n")

    stats_by_status = {"open": 0, "in_progress": 0, "in_review": 0, "done": 0, "closed": 0}
    stats_by_type = {"bug": 0, "feature": 0, "epic": 0}
    stats_by_priority = {"4": 0, "3": 0, "2": 0, "1": 0}

    for task in project.tasks:
        stats_by_status[task._status.value] += 1
        stats_by_type[task.label().strip("[]").lower()] += 1
        stats_by_priority[str(task.priority.value)] += 1

    report = f"По статусам:\n\
  OPEN          — {stats_by_status['open']}\n\
  IN_PROGRESS   — {stats_by_status['in_progress']}\n\
  IN_REVIEW     — {stats_by_status['in_review']}\n\
  DONE          — {stats_by_status['done']}\n\
  CLOSED        — {stats_by_status['closed']}\n\
По типам:\n\
  Bug           — {stats_by_type['bug']}\n\
  Feature       — {stats_by_type['feature']}\n\
  Epic          — {stats_by_type['epic']}\n\
По приоритетам:\n\
  CRITICAL      — {stats_by_priority['4']}\n\
  HIGH          — {stats_by_priority['3']}\n\
  MEDIUM        — {stats_by_priority['2']}\n\
  LOW           — {stats_by_priority['1']}\n"

    print(report)
    from task_tracker.cli import report_menu

    return report_menu
