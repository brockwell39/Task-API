import datetime
from typing import List
import strawberry
from strawberry import Schema
from sqlalchemy import select, text

from models import Task
from database import get_db


@strawberry.type
class TaskType:
    id: int
    title: str
    completed: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


def get_all_tasks(search: str | None = None) -> List[TaskType]:
    db = get_db()
    if search:
        searched_tasks = db.scalars(select(Task).from_statement(text(
            "SELECT * FROM tasks WHERE title LIKE '%"+search+"%'")))
        return [
            TaskType(
                id=task.id,
                title=task.title,
                completed=task.completed,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in searched_tasks
        ]
    else:
        all_tasks = db.query(Task).all()
        return [
            TaskType(
                id=task.id,
                title=task.title,
                completed=task.completed,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in all_tasks
        ]


def get_task(id: int) -> TaskType | None:
    db = get_db()
    task = db.get(Task, id)
    if task:
        return TaskType(
            id=task.id,
            title=task.title,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    else:
        return None


def get_all_incomplete_tasks() -> List[TaskType]:
    db = get_db()
    incomplete_tasks = db.scalars(select(Task).from_statement(text(
        "SELECT * FROM tasks WHERE completed = False ORDER BY created_at")))
    return [
        TaskType(
            id=task.id,
            title=task.title,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        for task in incomplete_tasks
    ]


@strawberry.type
class Query:
    tasks: List[TaskType] = strawberry.field(resolver=get_all_tasks)
    task: TaskType | None = strawberry.field(resolver=get_task)
    to_do_list: List[TaskType] = strawberry.field(resolver=get_all_incomplete_tasks)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_task(self, title: str) -> TaskType:
        db = get_db()
        task = Task(
            title=title,
            updated_at=datetime.datetime.now(),
            created_at=datetime.datetime.now()
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return TaskType(
            id=task.id,
            title=task.title,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )

    @strawberry.mutation
    def toggle_task(self, id: int) -> TaskType | None:
        db = get_db()
        task = db.get(Task, id)
        if task:
            task.completed = not task.completed
            task.updated_at = datetime.datetime.now()
            db.commit()
            db.refresh(task)
            return TaskType(
                id=task.id,
                title=task.title,
                completed=task.completed,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
        else:
            return None

    @strawberry.mutation
    def delete_task(self, id: int) -> TaskType | None:
        db = get_db()
        task = db.get(Task, id)
        if task:
            db.delete(task)
            db.commit()
            return TaskType(
                id=task.id,
                title=task.title,
                completed=task.completed,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
        else:
            return None

    @strawberry.mutation
    def urgent_task(self, id: int) -> TaskType | None:
        db = get_db()
        task = db.get(Task, id)
        if task:
            if not task.title[0:9] == "URGENT!!!":
                task.title = "URGENT!!! " + task.title
                task.updated_at = datetime.datetime.now()
                db.commit()
                db.refresh(task)
            return TaskType(
                id=task.id,
                title=task.title,
                completed=task.completed,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
        else:
            return None


schema = Schema(query=Query, mutation=Mutation)
