import imp
from fastapi import FastAPI
from routers import detail

app = FastAPI()

app.include_router(detail.router)
