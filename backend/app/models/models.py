from pydantic import Field, ConfigDict
from beanie import Document, Indexed
from typing import Annotated, Optional

from datetime import datetime, timezone


class User(Document):
    # основные данные
    name: Annotated[str, Indexed(unique=True)]
    hashed_password: str
    level: int = Field(default=1, gt=0)
    xp: float = Field(default=0, ge=0)
    Spoints: float = Field(default=0, ge=0)
    # подряд завершенные дни
    days_streak: int = Field(default=0, ge=0)
    last_streak: str | datetime = datetime.now().strftime("%Y-%m-%d")
    # множители и последний множитель
    mul: float = Field(default=1, ge=0)
    sale_shop: float = Field(default=1, ge=0)
    last_mul: str | datetime = datetime.now().strftime("%Y-%m-%d")
    # завершенные задания
    complete_simple_tasks: int = Field(default=0, ge=0)
    complete_common_tasks: int = Field(default=0, ge=0)
    complete_hard_tasks: int = Field(default=0, ge=0)
    complete_expert_tasks: int = Field(default=0, ge=0)
    complete_hardcore_tasks: int = Field(default=0, ge=0)

    model_config = ConfigDict(extra="forbid")

    class Settings:
        name = "users"


class BaseTask(Document):
    difficulty: Annotated[str, Indexed(unique=True)]
    points: int = Field(ge=0, description="Поинты за задание")

    model_config = ConfigDict(extra="forbid")

    class Settings:
        name = "baseTasks"


class Level(Document):
    level: Annotated[int, Indexed(unique=True)]
    xp: int = Field(ge=0, description="Требуемый опыт")
    role: str = Field(description="Роль пользователя")

    class Settings:
        name = "levels"


class ShopItem(Document):
    title: Annotated[str, Indexed(unique=True)] = Field(
        max_length=100, description="Название товара"
    )
    description: str = Field(max_length=255, description="Описание товара")
    price: int = Field(gt=0, description="Цена товара")
    type: str = Field(description="Тип товара")
    min_level: int = Field(gte=0, description="Минимальный уровень для покупки")

    model_config = ConfigDict(extra="forbid")

    class Settings:
        name = "shop_items"


class Task(Document):
    title: str = Field(max_length=100, description="Название задания")
    description: str = Field(max_length=255, description="Описание задания")
    type: str = Field(description="Тип задания")
    user: str = Field(description="Пользователь, который зарегистрировал задание")
    date: Optional[datetime] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    complete_date: Optional[datetime] = Field(default=None, description="Дата завершения задания")
    completed: bool = Field(default=False, description="Завершено задание")
    inactive: bool = Field(default=False, description="Истекло время")

    model_config = ConfigDict(extra="forbid")

    class Settings:
        name = "tasks"
