from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, tasks

models.Base.metadata.create_all(bind=engine)  # ← оставь закомментированным

app = FastAPI(  
    title="Task Manager Pro",
    description="API для управления задачами и пользователями",
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Task Manager Pro работает! 🚀"}