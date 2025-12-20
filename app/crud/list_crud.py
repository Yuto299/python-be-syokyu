from sqlalchemy.orm import Session

from app.models.list_model import ListModel


# GET Todoリスト
def get_todo_list(
    db: Session,
    todo_list_id: int,
):
    return db.query(ListModel).filter(ListModel.id == todo_list_id).first()


# POST Todoリスト
def post_todo_list(
    db: Session,
    title: str,
    description: str | None,
):
    new_list = ListModel(
        title=title,
        description=description,
    )
    db.add(new_list)
    db.commit()
    db.refresh(new_list)

    return new_list


# PUT Todoリスト
def put_todo_list(
    db: Session,
    todo_list_id: int,
    title: str,
    description: str | None,
):
    existing_list = db.query(ListModel).filter(ListModel.id == todo_list_id).first()

    existing_list.title = title
    if description is not None:
        existing_list.description = description

    db.commit()
    db.refresh(existing_list)

    return existing_list


# DELETE Todoリスト
def delete_todo_list(
    db: Session,
    todo_list_id: int,
):
    existing_list = db.query(ListModel).filter(ListModel.id == todo_list_id).first()

    db.delete(existing_list)
    db.commit()

    return {}


# GET Todoリスト一覧
def get_todo_lists(
    db: Session,
):
    return db.query(ListModel).all()
