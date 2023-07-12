from fastapi import FastAPI, Request, APIRouter
from starlette.staticfiles import StaticFiles

from routers import (
    table,
    users,
    craft,
    )

from view import views

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(table.router)
app.include_router(users.router)
app.include_router(craft.router)
app.include_router(views.router)

