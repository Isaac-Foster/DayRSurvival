from fastapi import FastAPI


from routers import table, users


app = FastAPI()

app.include_router(table.router)
app.include_router(users.router)