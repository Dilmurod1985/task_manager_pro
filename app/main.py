from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Task Manager Pro работает!"}
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router)
from .routers import users, tasks

app.include_router(users.router)
app.include_router(tasks.router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=10000, reload=True)
