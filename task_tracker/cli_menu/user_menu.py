from task_tracker.enums import Role
from task_tracker.models.base import Task
from task_tracker.models.user import User


def make_user() -> User:
    user_name = input("Введите имя исполнителя: ")
    default_role_str = "developer"
    user_input = input("Введите роль исполнителя [developer/qa/team_lead/pm]: ")
    user_role_str = user_input if user_input else default_role_str
    user_role = Role(user_role_str)

    user = User(user_name, user_role)

    print(f"Пользователь {user_name} с ролью {user_role_str} создан.\n")
    return user


def make_new_user():
    make_user()

    from task_tracker.cli import users_menu
    return users_menu


def show_user():
    user_name = input("Введите имя исполнителя: ")
    if user := User.users.get(user_name):
        print(user.full_display())
    else:
        print("Ошибка: Исполнителя с таким именем не существует!\n")

    from task_tracker.cli import users_menu

    return users_menu


def delete_user():
    user_name = input("Введите имя исполнителя: ")
    print(User.users.pop(user_name, "Пользователя с таким именем нет\n"))
    from task_tracker.cli import users_menu

    return users_menu


def tasks_by_asignee():
    print("=== Задачи по исполнителям ===\n")

    for name, user in User.users.items():
        print(f"{name} ({user.role}):\n")
        user_tasks = [task.short_display() for task in Task.tasks.values() if task.assignee == name]
        for i, task in enumerate(user_tasks):
            print(f"\t{i} {task}\n")

    unknow_asigners = [task.short_display() for task in Task.tasks.values() if not task.assignee]

    print("Не назначены:\n")
    for i, task in enumerate(unknow_asigners):
        print(f"\t{i} {task}\n")

    from task_tracker.cli import report_menu

    return report_menu
