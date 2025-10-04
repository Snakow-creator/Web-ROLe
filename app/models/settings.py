from pydantic_settings import BaseSettings
from pydantic import Field


class InputSettings(BaseSettings):
    mongo_url: str = Field(validation_alias="MONGO_URL")
    collection_name: str = Field(validation_alias="COLLECTION_NAME")
    test_collection_name: str = Field(validation_alias="TEST_COLLECTION_NAME")

    class Config:
        env_file = ".env"

baseSettings = InputSettings()

class Settings:
    def __init__(self):
        self.mongo_url: str = baseSettings.mongo_url
        self.collection_name: str = baseSettings.test_collection_name

settings = Settings()
