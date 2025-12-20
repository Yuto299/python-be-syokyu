from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import list_crud
from app.dependencies import get_db
from app.schemas.list_schema import NewTodoList, ResponseTodoList, UpdateTodoList

router = APIRouter(prefix="/lists", tags=["Todoリスト"])


@router.get("/{todo_list_id}", response_model=ResponseTodoList)
def get_todo_list(
    todo_list_id: int,
    db: Session = Depends(get_db),
):
    todo_list = list_crud.get_todo_list(db, todo_list_id)
    if not todo_list:
        raise HTTPException(status_code=404, detail="Todo List not found")
    return todo_list


@router.post("/", response_model=ResponseTodoList, status_code=201)
def post_todo_list(
    todo_list: NewTodoList,
    db: Session = Depends(get_db),
):
    return list_crud.post_todo_list(db, todo_list.title, todo_list.description)


@router.put("/{todo_list_id}", response_model=ResponseTodoList)
def put_todo_list(
    todo_list_id: int,
    todo_list: UpdateTodoList,
    db: Session = Depends(get_db),
):
    if todo_list.title is None:
        raise HTTPException(status_code=401, detail="Title is required")

    existing_list = list_crud.put_todo_list(
        db,
        todo_list_id,
        todo_list.title,
        todo_list.description,
    )
    if not existing_list:
        raise HTTPException(status_code=404, detail="Todo List not found")
    return existing_list


@router.delete("/{todo_list_id}")
def delete_todo_list(
    todo_list_id: int,
    db: Session = Depends(get_db),
):
    existing_list = list_crud.delete_todo_list(db, todo_list_id)
    if not existing_list:
        raise HTTPException(status_code=404, detail="Todo List not found")
    return {}


@router.get("/", response_model=list[ResponseTodoList])
def get_todo_lists(
    db: Session = Depends(get_db),
):
    return list_crud.get_todo_lists(db)
