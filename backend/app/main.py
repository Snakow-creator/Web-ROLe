from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager

from models.models import User, Level, ShopItem, BaseTask, Task
from base.utils import drop_tests_collection
from models.settings import settings, baseSettings
from routers import core

import beanie
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def main(app: FastAPI):
    client = AsyncIOMotorClient(settings.mongo_url)
    collection = settings.collection_name
    await beanie.init_beanie(
        database=client[collection],
        document_models=[User, Level, ShopItem, BaseTask, Task],
    )
    logging.info("ROLe is starting...")
    yield
    if collection == baseSettings.test_collection_name:
        await drop_tests_collection()
    logging.info("ROLe is closing...")


origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "https://127.0.0.1:5173",
    "https://localhost:5173",
]

app = FastAPI(lifespan=main)
app.include_router(core.init_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # используем только проверенные адреса
    allow_credentials=True,  # отправка cookies, токенов, авторизационных заголовков
    allow_methods=["*"],  # использование всех методов(GET, POST, PUT, DELETE)
    allow_headers=["*"],  # любые headers
)

if __name__ == "__main__" :
    settings.collection_name = baseSettings.collection_name
    uvicorn.run(app, host="localhost", port=7878)
