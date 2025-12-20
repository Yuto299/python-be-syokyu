from datetime import datetime

from sqlalchemy.orm import Session

from app.const import TodoItemStatusCode
from app.models.item_model import ItemModel


# GET Todo項目
def get_todo_item(
    db: Session,
    todo_list_id: int,
    todo_item_id: int,
):
    return (
        db.query(ItemModel)
        .filter(ItemModel.id == todo_item_id, ItemModel.todo_list_id == todo_list_id)
        .first()
    )


# POST Todo項目
def post_todo_item(
    db: Session,
    todo_list_id: int,
    title: str,
    description: str | None,
    due_at: datetime | None,
):
    from app.crud import list_crud

    # todo_list_idの存在チェック
    todo_list = list_crud.get_todo_list(db, todo_list_id)
    if not todo_list:
        return None

    new_item = ItemModel(
        todo_list_id=todo_list_id,
        title=title,
        description=description,
        status_code=TodoItemStatusCode.NOT_COMPLETED.value,
        due_at=due_at,
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


# PUT Todo項目
def put_todo_item(
    db: Session,
    todo_list_id: int,
    todo_item_id: int,
    title: str,
    description: str | None,
    due_at: datetime | None,
    complete: bool | None,
):
    existing_item = (
        db.query(ItemModel)
        .filter(ItemModel.id == todo_item_id, ItemModel.todo_list_id == todo_list_id)
        .first()
    )

    if not existing_item:
        return None

    existing_item.title = title

    if description is not None:
        existing_item.description = description
    if due_at is not None:
        existing_item.due_at = due_at
    if complete is not None:
        existing_item.status_code = (
            TodoItemStatusCode.COMPLETED.value
            if complete
            else TodoItemStatusCode.NOT_COMPLETED.value
        )

    db.commit()
    db.refresh(existing_item)

    return existing_item


# DELETE Todo項目
def delete_todo_item(
    db: Session,
    todo_list_id: int,
    todo_item_id: int,
):
    existing_item = (
        db.query(ItemModel)
        .filter(ItemModel.id == todo_item_id, ItemModel.todo_list_id == todo_list_id)
        .first()
    )

    if not existing_item:
        return None

    db.delete(existing_item)
    db.commit()

    return {}


# GET Todo項目一覧
def get_todo_items(
    db: Session,
    todo_list_id: int,
):
    return db.query(ItemModel).filter(ItemModel.todo_list_id == todo_list_id).all()
