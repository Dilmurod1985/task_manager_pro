from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/tasks", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    db_task = models.Task(**task.dict(), user_id=user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks", response_model=list[schemas.TaskOut])
def get_tasks(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.query(models.Task).filter(models.Task.user_id == user.id).all()

@router.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    db.delete(db_task)
    db.commit()
    return {"detail": "Задача удалена"}
