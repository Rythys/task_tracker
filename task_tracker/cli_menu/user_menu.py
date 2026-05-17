from task_tracker import global_states
from task_tracker.enums import set_role_from_str
from task_tracker.models.user import User


def make_user() -> User:
    user_name = input("Введите имя исполнителя: ")
    default_role_str = "developer"
    user_input = input("Введите роль исполнителя [developer/qa/team_lead/pm]: ")
    user_role_str = user_input if user_input else default_role_str
    user_role = set_role_from_str(user_role_str)

    user = User(user_name, user_role)
    global_states.users[user_name] = user
    global_states.users_by_id[user.id] = user

    print(f"Пользователь {user_name} с ролью {user_role_str} создан.\n")
    return user


def make_new_user():
    make_user()

    from task_tracker.cli import users_menu
    return users_menu


def show_user():
    user_name = input("Введите имя исполнителя: ")
    if user := global_states.users.get(user_name):
        print(user.full_display())
    else:
        print("Ошибка: Исполнителя с таким именем не существует!\n")

    from task_tracker.cli import users_menu

    return users_menu


def delete_user():
    user_name = input("Введите имя исполнителя: ")
    print(global_states.users.pop(user_name, "Пользователя с таким именем нет\n"))
    from task_tracker.cli import users_menu

    return users_menu


def tasks_by_asignee():
    print("=== Задачи по исполнителям ===\n")

    for name, user in global_states.users.items():
        print(f"{name} ({user.role}):\n")
        user_tasks = [task.short_display() for task in global_states.tasks if task.assignee == name]
        for i, task in enumerate(user_tasks):
            print(f"\t{i} {task}\n")

    unknow_asigners = [task.short_display() for task in global_states.tasks if not task.assignee]

    print("Не назначены:\n")
    for i, task in enumerate(unknow_asigners):
        print(f"\t{i} {task}\n")

    from task_tracker.cli import report_menu

    return report_menu
