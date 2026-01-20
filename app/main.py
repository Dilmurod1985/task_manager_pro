from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, tasks

# Создание таблиц в базе данных
models.Base.metadata.create_all(bind=engine)

# Инициализация приложения
app = FastAPI(
    title="Task Manager Pro",
    description="API для управления задачами и пользователями",
    version="1.0.0"
)

# Подключение роутеров
app.include_router(users.router)
app.include_router(tasks.router)

# Базовый маршрут для проверки
@app.get("/")
def root():
    return {"message": "Task Manager Pro работает! 🚀"}

