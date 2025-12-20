from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import item_crud
from app.dependencies import get_db
from app.schemas.item_schema import NewTodoItem, ResponseTodoItem, UpdateTodoItem

router = APIRouter(prefix="/lists/{todo_list_id}/items", tags=["Todo項目"])


@router.get("/{todo_item_id}", response_model=ResponseTodoItem)
def get_todo_item(
    todo_list_id: int,
    todo_item_id: int,
    db: Session = Depends(get_db),
):
    todo_item = item_crud.get_todo_item(db, todo_list_id, todo_item_id)
    if not todo_item:
        raise HTTPException(status_code=404, detail="Todo Item not found")
    return todo_item


@router.post("/", response_model=ResponseTodoItem, status_code=201)
def post_todo_item(
    todo_list_id: int,
    todo_item: NewTodoItem,
    db: Session = Depends(get_db),
):
    new_item = item_crud.post_todo_item(
        db,
        todo_list_id,
        todo_item.title,
        todo_item.description,
        todo_item.due_at,
    )
    if not new_item:
        raise HTTPException(status_code=404, detail="Todo List not found")
    return new_item


@router.put("/{todo_item_id}", response_model=ResponseTodoItem)
def put_todo_item(
    todo_list_id: int,
    todo_item_id: int,
    todo_item: UpdateTodoItem,
    db: Session = Depends(get_db),
):
    existing_item = item_crud.put_todo_item(
        db,
        todo_list_id,
        todo_item_id,
        todo_item.title,
        todo_item.description,
        todo_item.due_at,
        todo_item.complete,
    )
    if not existing_item:
        raise HTTPException(status_code=404, detail="Todo Item not found")
    return existing_item


@router.delete("/{todo_item_id}")
def delete_todo_item(
    todo_list_id: int,
    todo_item_id: int,
    db: Session = Depends(get_db),
):
    existing_item = item_crud.delete_todo_item(db, todo_list_id, todo_item_id)
    if not existing_item:
        raise HTTPException(status_code=404, detail="Todo Item not found")
    return {}


@router.get("/", response_model=list[ResponseTodoItem])
def get_todo_items(
    todo_list_id: int,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 10,
):
    return item_crud.get_todo_items(db, todo_list_id, page, per_page)
