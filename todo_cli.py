"""A small command-line todo tool for Git practice."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA_FILE = Path(__file__).with_name("tasks.json")


def load_tasks() -> list[dict]:
    """Load tasks from the local JSON file."""
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_tasks(tasks: list[dict]) -> None:
    """Persist tasks to the local JSON file."""
    DATA_FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def add_task(title: str) -> None:
    """Add one task with an auto-incrementing id."""
    tasks = load_tasks()
    next_id = max((task["id"] for task in tasks), default=0) + 1
    tasks.append({"id": next_id, "title": title, "done": False})
    save_tasks(tasks)
    print(f"Added task #{next_id}: {title}")


def list_tasks(show_all: bool) -> None:
    """Print tasks to the terminal."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet. Use 'add' to create one.")
        return

    for task in tasks:
        if not show_all and task["done"]:
            continue
        status = "x" if task["done"] else " "
        print(f"[{status}] {task['id']}: {task['title']}")


def mark_done(task_id: int) -> None:
    """Mark one task as completed."""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"Completed task #{task_id}")
            return
    print(f"Task #{task_id} was not found.")


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Simple todo tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a task")
    add_parser.add_argument("title", help="Task title")

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument(
        "--all",
        action="store_true",
        help="Show completed tasks as well",
    )

    done_parser = subparsers.add_parser("done", help="Complete a task")
    done_parser.add_argument("task_id", type=int, help="Task id")

    return parser


def main() -> None:
    """Run the command-line interface."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        add_task(args.title)
    elif args.command == "list":
        list_tasks(show_all=args.all)
    elif args.command == "done":
        mark_done(args.task_id)


if __name__ == "__main__":
    main()
