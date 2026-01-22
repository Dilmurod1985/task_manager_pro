from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

# Один раз создаём Base здесь (НЕ импортируем из database!)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связь с задачами
    tasks = relationship("Task", back_populates="owner")
class Task(Base):
    __tablename__ = "tasks"
    # ... ваши поля ...

    # Внешний ключ остается таким же
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Уточняем связь явно:
    owner = relationship("User", back_populates="tasks", foreign_keys=[user_id])
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Внешний ключ
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Обратная связь
    owner = relationship("User", back_populates="tasks")