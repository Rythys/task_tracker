"""Точка входа приложения.

Запуск:
    python -m task_tracker.main [--data FILE]
    python -m task_tracker [--data FILE]
"""

import argparse

from task_tracker.cli import run_cli


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Разобрать аргументы командной строки.

    Аргументы:
        --data FILE: путь к файлу данных (по умолчанию data.json)

    Args:
        args: список аргументов (None = sys.argv[1:])

    Returns:
        argparse.Namespace с полем data
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default="data.json")
    parsed_args = parser.parse_args(args)
    return parsed_args


def main() -> None:
    """Главная функция: парсинг аргументов → запуск CLI."""

    inp_args = parse_args()
    run_cli(inp_args.data)


if __name__ == "__main__":
    main()
