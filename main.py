from fastapi import FastAPI
from database import init_db
from routes import users, projects

app = FastAPI()

init_db()

app.include_router(users.router)
app.include_router(projects.router)
