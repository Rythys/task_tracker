from task_tracker import global_states
from task_tracker.cli_menu.user_menu import make_user
from task_tracker.enums import (
    priority_to_str,
    set_prority_from_str,
    set_status_from_str,
)
from task_tracker.models.tasks import Bug, Epic, Feature


def delete_task():
    task_title = input("Введите название задачи: ")
    print(global_states.tasks.pop(task_title, "Задач с таким названием нет"))
    from task_tracker.cli import tasks_menu

    return tasks_menu


def show_task_details():
    task_title = input("Введите название задачи: ")
    if task := global_states.tasks.get(task_title):
        print(task.full_display())
    else:
        print("\nОшибка: Задачи с таким названем не существует!\n")
    from task_tracker.cli import tasks_menu

    return tasks_menu


def assign_user():
    user = None
    if input("Добавить существующего исполнителя? [y/n] ") == "n":
        user = make_user()
    else:
        user_name = input("Введите имя исполнителя: ")
        user = global_states.users.get(user_name)
    task_title = input("Введите название задачи: ")
    if global_states.tasks.get(task_title):
        global_states.tasks[task_title].assignee = user
        print(
            f"{global_states.tasks[task_title].assignee} назначен исполнителем проекта {task_title}"
        )
    else:
        print("Ошибка: Задач с таким названием не существует!\n")

    from task_tracker.cli import tasks_menu

    return tasks_menu


def change_task_status():
    task_title = input("Введите название задачи: ")
    new_status_str = input("Введите новый статус: ")

    new_status = set_status_from_str(new_status_str)
    global_states.tasks[task_title].change_status(new_status)

    from task_tracker.cli import tasks_menu

    return tasks_menu


def filtered_tasks_list():
    print("Фильтры:")

    status_str = input("Статус [open/in_progress/in_review/done/closed]: ")
    priority = input("Приоритет [low/medium/high/critical]: ")
    tasks_type = input("Тип [bug/feature/epic]: ")
    assignee = input("Исполнитель (имя): ")
    sort_tasks_by = input("Сортировка [priority/created_at/estimate]: ")

    filtered_tasks = []

    for task in global_states.tasks.values():
        if status_str and task._status.value != status_str:
            continue
        if priority and task.priority != set_prority_from_str(priority):
            continue
        if tasks_type and task.label().strip("[]").lower() != tasks_type:
            continue
        if assignee and (not task.assignee or task.assignee.name != assignee):
            continue
        filtered_tasks.append(task)
    if not sort_tasks_by or filtered_tasks and sort_tasks_by == "priority":
        filtered_tasks.sort(key=lambda t: t.priority.value, reverse=True)
        for task in filtered_tasks:
            print(f"{priority_to_str(task.priority)}: {task.short_display()}\n")

    if filtered_tasks and sort_tasks_by == "created_at":
        filtered_tasks.sort(key=lambda t: t.created_at)
        for task in filtered_tasks:
            print(f"{task.created_at}: {task.short_display()}\n")
    print(filtered_tasks)
    if filtered_tasks and sort_tasks_by == "estimate":
        filtered_tasks.sort(key=lambda t: t.estimate(), reverse=True)
        for task in filtered_tasks:
            print(f"{task.estimate}: {task.short_display()}\n")

    from task_tracker.cli import tasks_menu

    return tasks_menu


def make_task():
    task_title, task = make_subtask()
    if task:
        global_states.tasks[task_title] = task
    from task_tracker.cli import tasks_menu

    return tasks_menu


def make_subtask():
    task = None
    task_title = input("Введите название задачи: ")
    task_description = input("Введите описание задачи: ")
    default_type = "medium"

    user_input = input(f"Введите приоритетность задачи (low, medium, high) [{default_type}]: ")
    task_priority_str = user_input if user_input else default_type
    task_priority = set_prority_from_str(task_priority_str)

    task_type = input("Введите тип задачи (bug, feature, epic): ")
    if task_type == "bug":
        default_severity = 1
        user_input = input(f"Введите критичность задачи (1-10) [{default_severity}]: ")
        severity = int(user_input) if user_input else default_severity

        default_steps = ""
        user_input = input("Введите шаги для воспроизведения бага: ")
        steps_to_reproduce = user_input if user_input else default_steps

        task = Bug(task_title, task_description, task_priority, severity, steps_to_reproduce)

    if task_type == "feature":
        default_business_value = 5
        user_input = input(f"Введите ценность для бизнеса [{default_business_value}]: ")
        business_value = int(user_input) if user_input else default_business_value

        default_complexity = 5
        user_input = input(f"Введите сложность задачи [{default_complexity}]: ")
        complexity = int(user_input) if user_input else default_complexity

        task = Feature(task_title, task_description, task_priority, business_value, complexity)

    if task_type == "epic":
        subtasks = None
        default_subtasks = "n"
        is_subtasks = "y"
        while is_subtasks == "y":
            user_input = input("Добавить подзадачу? [y/n]: ")
            is_subtasks = user_input if user_input else default_subtasks
            if is_subtasks != "y":
                break
            if not subtasks:
                subtasks = []
            (subtask_title, subtask) = make_subtask()
            subtasks.append(subtask)

        task = Epic(task_title, task_description, task_priority, subtasks)

    return task_title, task


def etimate_report():
    print("=== Оценка трудоёмкости ===\n")
    bug_estimate_sum = sum(
        map(
            lambda t: t.estimate(),
            filter(lambda t: t.label() == "[BUG]", global_states.tasks.values()),
        )
    )
    feature_estimate_sum = sum(
        map(
            lambda t: t.estimate(),
            filter(lambda t: t.label() == "[FEATURE]", global_states.tasks.values()),
        )
    )
    epic_estimate_sum = sum(
        map(
            lambda t: t.estimate(),
            filter(lambda t: t.label() == "[EPIC]", global_states.tasks.values()),
        )
    )

    estimations_sum = bug_estimate_sum + feature_estimate_sum + epic_estimate_sum

    etimate_top_5 = list(global_states.tasks.values())
    if etimate_top_5:
        etimate_top_5.sort(key=lambda t: t.estimate(), reverse=True)[: len(etimate_top_5)]

    print(
        f"Общая оценка: {estimations_sum} часов\n\
    По типам:\n\
    Bug       — {bug_estimate_sum} ч\n\
    Feature   — {feature_estimate_sum} ч\n\
    Epic      — {epic_estimate_sum} ч\n\
    "
    )
    print("Топ-5 самых трудоёмких:\n")
    for task in enumerate(etimate_top_5):
        print(f"{task.label()} {task.title} — {task.estimate} ч\n")

    from task_tracker.cli import report_menu

    return report_menu
