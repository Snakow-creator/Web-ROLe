from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    name: str = Field(max_length=20, description="Имя пользователя")
    password: str = Field(min_length=8, max_length=20, description="Пароль пользователя")


class RegisterUserSchema(BaseModel):
    name: str = Field(max_length=20, description="Имя пользователя")
    password1: str = Field(min_length=8, max_length=20, description="Пароль")
    password2: str = Field(min_length=8, max_length=20, description="Подтвердите пароль")


class TaskSchema(BaseModel):
    title: str = Field(max_length=100, description="Название задания")
    description: str = Field(max_length=255, description="Описание задания")
    type: str = Field(description="Тип задания")
