from fastapi import FastAPI


from routers.test import router


app = FastAPI()

app.include_router(router, prefix="")