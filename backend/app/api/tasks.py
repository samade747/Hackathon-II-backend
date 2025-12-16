from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, or_, col
from app.db import get_session
from app.models import Task
from app.schemas import TaskCreate, TaskRead, TaskUpdate
from app.auth import get_current_user_id, verify_user_access

router = APIRouter()


@router.get("/{user_id}/tasks", response_model=List[TaskRead])
def list_tasks(
    user_id: str,
    status_filter: Optional[str] = Query(None, alias="status"),
    priority: Optional[str] = None,
    tag: Optional[str] = None,
    q: Optional[str] = None,
    sort_by: str = Query("created_at"),
    order: str = Query("asc"),
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    verify_user_access(current_user_id, user_id)

    query = select(Task).where(Task.user_id == user_id)

    if status_filter:
        query = query.where(Task.status == status_filter)

    if priority:
        query = query.where(Task.priority == priority)

    if tag:
        query = query.where(Task.tags.contains(tag))

    if q:
        query = query.where(
            or_(
                Task.title.contains(q),
                Task.description.contains(q)
            )
        )

    sort_column = getattr(Task, sort_by, Task.created_at)
    if order == "desc":
        sort_column = col(sort_column).desc()
    else:
        sort_column = col(sort_column).asc()

    query = query.order_by(sort_column)

    tasks = session.exec(query).all()
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    verify_user_access(current_user_id, user_id)

    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        tags=task_data.tags,
        due_date=task_data.due_date,
        is_recurring=task_data.is_recurring or False,
        recurrence_rule=task_data.recurrence_rule,
    )

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskRead)
def get_task(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    verify_user_access(current_user_id, user_id)

    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskRead)
def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    verify_user_access(current_user_id, user_id)

    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    verify_user_access(current_user_id, user_id)

    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return None


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskRead)
def toggle_task_completion(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    verify_user_access(current_user_id, user_id)

    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = "done" if task.status == "open" else "open"
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task
