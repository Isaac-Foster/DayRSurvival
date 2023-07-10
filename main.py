from fastapi import FastAPI


from routers import (
    table,
    users,
    craft
    )


app = FastAPI()

app.include_router(table.router)
app.include_router(users.router)
app.include_router(craft.router)