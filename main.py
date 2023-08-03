from fastapi import FastAPI

from order import models
from order.database import engine
from order.routers import order, account, authentication

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(account.router)
app.include_router(authentication.router)
app.include_router(order.router)
