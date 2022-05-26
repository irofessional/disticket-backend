import imp
from fastapi import FastAPI
from routers import detail, healthcheck

app = FastAPI()

app.include_router(detail.router)
app.include_router(healthcheck.router)
