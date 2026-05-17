"""Логика интерактивного меню.

Модуль отвечает за взаимодействие с пользователем через консоль:
главное меню, подменю, ввод данных, вывод отчётов.
"""

from task_tracker import global_states
from task_tracker.cli_menu.project_menu import delete_project, make_project, project_report
from task_tracker.cli_menu.task_menu import (
    assign_user,
    change_task_status,
    delete_task,
    etimate_report,
    filtered_tasks_list,
    make_task,
    show_task_details,
)
from task_tracker.cli_menu.user_menu import delete_user, make_new_user, show_user, tasks_by_asignee
from task_tracker.storage import load_data, save_data


def users_menu():
    user_menu = "\n=== Исполнители ===\n\n\
1. Создать исполнителя\n\
2. Удалить исполнителя\n\
3. Показать информацию об исполнителе\n\
4. Назад\n"
    print(user_menu)

    menu_choice = input("Выберите действие: ")
    if menu_choice == "1":
        return make_new_user
    if menu_choice == "2":
        return delete_user
    if menu_choice == "3":
        return show_user
    if menu_choice == "4":
        return main_menu
    return users_menu


def projects_menu():
    report_menu = "\n=== Проекты ===\n\n\
1. Создать проект\n\
2. Удалить проект\n\
3. Назад\n"
    print(report_menu)

    menu_choice = input("Выберите действие: ")
    if menu_choice == "1":
        return make_project
    if menu_choice == "2":
        return delete_project
    if menu_choice == "3":
        return main_menu
    return projects_menu


def tasks_menu():
    task_control_menu = "\n=== Задачи ===\n\n\
1. Создать задачу\n\
2. Список задач (с фильтрами)\n\
3. Изменить статус задачи\n\
4. Назначить исполнителя\n\
5. Показать детали задачи\n\
6. Удалить задачу\n\
7. Назад\n"
    print(task_control_menu)

    menu_choice = input("Выберите действие: ")
    if menu_choice == "1":
        return make_task
    if menu_choice == "2":
        return filtered_tasks_list
    if menu_choice == "3":
        return change_task_status
    if menu_choice == "4":
        return assign_user
    if menu_choice == "5":
        return show_task_details
    if menu_choice == "6":
        return delete_task
    if menu_choice == "7":
        return main_menu
    return tasks_menu


def report_menu():
    report_menu = "\n=== Отчёты ===\n\n\
1. Сводка по проекту\n\
2. Задачи по исполнителям\n\
3. Оценка трудоёмкости\n\
4. Назад\n"
    print(report_menu)

    menu_choice = input("Выберите действие: ")
    if menu_choice == "1":
        return project_report
    if menu_choice == "2":
        return tasks_by_asignee
    if menu_choice == "3":
        return etimate_report
    if menu_choice == "4":
        return main_menu
    return report_menu


def main_menu():
    main_menu = "\n=== Task Tracker ===\n\n\
1. Управление проектами\n\
2. Управление пользователями\n\
3. Управление задачами\n\
4. Отчёты\n\
5. Сохранить и выйти\n"
    print(main_menu)

    menu_choice = input("Выберите действие: ")
    if menu_choice == "1":
        return projects_menu
    if menu_choice == "2":
        return users_menu
    if menu_choice == "3":
        return tasks_menu
    if menu_choice == "4":
        return report_menu
    if menu_choice == "5":
        return save_data
    return main_menu


def run_cli(data_file: str = "data.json") -> None:
    """Запустить интерактивное меню.

    Главное меню:
        1. Управление проектами
        2. Управление пользователями
        3. Управление задачами
        4. Отчёты
        5. Сохранить и выйти

    Требования:
    - Загрузить данные из data_file при старте
    - При выходе — сохранить данные
    - Некорректный ввод → повторный запрос (без краша)
    - Все ошибки обрабатываются с понятным сообщением

    Args:
        data_file: путь к файлу данных
    """

    load_data(data_file)

    current_screen = main_menu
    while current_screen is not None or current_screen:
        if current_screen == save_data:
            save_data(global_states.projects.values(), data_file)
            print("Данные сохранены. Выход.")
            break
        current_screen = current_screen()
