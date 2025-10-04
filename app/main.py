from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager

from models.models import User, Level, ShopItem, BaseTask
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
        document_models=[User, Level, ShopItem, BaseTask],
    )
    if collection == "test_role_db":
        await drop_tests_collection()

    logging.info("ROLe is starting...")
    yield
    logging.info("ROLe is closing...")


app = FastAPI(lifespan=main)
app.include_router(core.init_router)
logging.warning("app is load")

if __name__ == "__main__":
    settings.collection_name = baseSettings.collection_name
    uvicorn.run(app, host="localhost", port=7878)
