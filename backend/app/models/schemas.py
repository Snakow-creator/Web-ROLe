from pydantic import BaseModel, Field, ConfigDict


class UserSchema(BaseModel):
    name: str = Field(max_length=20, description="Имя пользователя")
    password: str = Field(min_length=8, max_length=20, description="Пароль пользователя")


class RegisterUserSchema(BaseModel):
    name: str = Field(max_length=20, description="Имя пользователя")
    password1: str = Field(min_length=8, max_length=20, description="Пароль")
    password2: str = Field(min_length=8, max_length=20, description="Подтвердите пароль")
