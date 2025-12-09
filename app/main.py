import os
from datetime import datetime

from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.const import TodoItemStatusCode

from .dependencies import get_db
from .models.item_model import ItemModel
from .models.list_model import ListModel

DEBUG = os.environ.get("DEBUG", "") == "true"

app = FastAPI(
    title="Python Backend Stations",
    debug=DEBUG,
)

if DEBUG:
    from debug_toolbar.middleware import DebugToolbarMiddleware

    # panelsに追加で表示するパネルを指定できる
    app.add_middleware(
        DebugToolbarMiddleware,
        panels=["app.database.SQLAlchemyPanel"],
    )


class NewTodoItem(BaseModel):
    """TODO項目新規作成時のスキーマ."""

    title: str = Field(title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(
        default=None, title="Todo Item Description", min_length=1, max_length=200
    )
    due_at: datetime | None = Field(default=None, title="Todo Item Due")


class UpdateTodoItem(BaseModel):
    """TODO項目更新時のスキーマ."""

    title: str | None = Field(
        default=None, title="Todo Item Title", min_length=1, max_length=100
    )
    description: str | None = Field(
        default=None, title="Todo Item Description", min_length=1, max_length=200
    )
    due_at: datetime | None = Field(default=None, title="Todo Item Due")
    complete: bool | None = Field(
        default=None, title="Set Todo Item status as completed"
    )


class ResponseTodoItem(BaseModel):
    id: int
    todo_list_id: int
    title: str = Field(title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(
        default=None, title="Todo Item Description", min_length=1, max_length=200
    )
    status_code: TodoItemStatusCode = Field(title="Todo Status Code")
    due_at: datetime | None = Field(default=None, title="Todo Item Due")
    created_at: datetime = Field(title="datetime that the item was created")
    updated_at: datetime = Field(title="datetime that the item was updated")


class NewTodoList(BaseModel):
    """TODOリスト新規作成時のスキーマ."""

    title: str = Field(title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(
        default=None, title="Todo List Description", min_length=1, max_length=200
    )


class UpdateTodoList(BaseModel):
    """TODOリスト更新時のスキーマ."""

    title: str | None = Field(
        default=None, title="Todo List Title", min_length=1, max_length=100
    )
    description: str | None = Field(
        default=None, title="Todo List Description", min_length=1, max_length=200
    )


class ResponseTodoList(BaseModel):
    """TODOリストのレスポンススキーマ."""

    id: int
    title: str = Field(title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(
        default=None, title="Todo List Description", min_length=1, max_length=200
    )
    created_at: datetime = Field(title="datetime that the item was created")
    updated_at: datetime = Field(title="datetime that the item was updated")


# GET Hello
@app.get("/echo", tags=["Hello"])
def get_echo(message: str, name: str):

    return {"Message": f"{message} {name}!"}


# GET System
@app.get("/health", tags=["System"])
def get_health():
    return {"status": "ok"}


# GET Todoリスト
@app.get("/lists/{todo_list_id}", response_model=ResponseTodoList, tags=["Todoリスト"])
def get_todo_list(
    todo_list_id: int,
    db: Session = Depends(get_db),
):
    todo_list = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    return todo_list


# POST Todoリスト
@app.post("/lists", response_model=ResponseTodoList, tags=["Todoリスト"])
def post_todo_list(
    todo_list: NewTodoList,
    db: Session = Depends(get_db),
):
    new_list = ListModel(
        title=todo_list.title,
        description=todo_list.description,
    )
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return new_list
