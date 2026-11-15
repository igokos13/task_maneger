from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.base import get_engine
from models.models import Category, Task


def _category_to_dict(category: Category) -> dict:
    return {"id": category.id, "name": category.name}


# READ (список)
def list_categories() -> list[dict]:
    with Session(get_engine()) as session:
        categories = session.scalars(select(Category).order_by(Category.name))
        return [_category_to_dict(category) for category in categories]


# READ (одна категория)
def get_category(category_id: int) -> dict | None:
    with Session(get_engine()) as session:
        category = session.get(Category, category_id)
        return _category_to_dict(category) if category is not None else None


# CREATE
def create_category(category: dict) -> int:
    with Session(get_engine()) as session, session.begin():
        new_category = Category(name=category["name"])
        session.add(new_category)
        session.flush()  # чтобы получить id новой записи
        return new_category.id


# UPDATE
def update_category(category_id: int, category: dict) -> None:
    with Session(get_engine()) as session, session.begin():
        db_category = session.get(Category, category_id)
        if db_category is not None:
            db_category.name = category["name"]


# вспомогательная функция для DELETE: сколько задач связано с категорией
def count_category_tasks(category_id: int) -> int:
    with Session(get_engine()) as session:
        return session.scalar(
            select(func.count()).select_from(Task).where(Task.category_id == category_id)
        )


# DELETE
def delete_category(category_id: int) -> None:
    with Session(get_engine()) as session, session.begin():
        db_category = session.get(Category, category_id)
        if db_category is not None:
            session.delete(db_category)