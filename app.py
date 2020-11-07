from fastapi import FastAPI

from amqp import amqp_handler
from routes import router

app = FastAPI()

app.include_router(router)


@app.on_event('startup')
async def startup():
    await amqp_handler.init()
