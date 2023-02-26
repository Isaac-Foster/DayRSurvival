from fastapi import FastAPI


from routers import table


app = FastAPI()

app.include_router(table.router)