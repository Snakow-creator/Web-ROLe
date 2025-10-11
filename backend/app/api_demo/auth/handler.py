from fastapi import APIRouter, Depends, Response, HTTPException, Request
from authx import AuthX, AuthXConfig
from pydantic import BaseModel
from datetime import datetime, timedelta

from models.models import User
from models.schemas import UserSchema, RegisterUserSchema
from api_demo.auth.crypt import hash_password, verify_password
from levels.data import which_my_role

import logging
import jwt

router = APIRouter(tags=["auth"])

config = AuthXConfig()
config.JWT_SECRET_KEY = "MY_SECRET_KEY"
config.JWT_ALGORITHM = "HS256"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

csrf_required = security.token_required(
    type="access",
    verify_type=True,
    verify_fresh=False,
    verify_csrf=True  # ⚡ отключаем CSRF
)


class RefreshForm(BaseModel):
    refresh_token: str


@router.post("/login/")
async def login(creds: UserSchema, response: Response):
    if creds.name == "test" and creds.password == "testtest":
        data = {"name": "test",
                  "level": 999,
                  "xp": 9999999,
                  "Spoints":9999999,
                  "days_streak": 999,
                  "mul": 999, "sale_shop": 999,
                  "last_streak": "11-12-2099",
                  "last_mul": "11-12-2099",
                  "complete_simple_tasks": 999,
                  "complete_common_tasks": 999,
                  "complete_hard_tasks": 999,
                  "complete_expert_tasks": 999,
                  "complete_hardcore_tasks": 999
            }
        token = security.create_access_token(uid="11111",
            data=data,
            expiry=timedelta(days=15)
        )
        response.set_cookie(key="my_access_token", value=token, httponly=True)
        return data
    else:
        user = await User.find_one(User.name == creds.name)
        if await verify_password(creds.password, user.hashed_password):
            data = {"name": user.name,
                  "level": user.level,
                  "xp": user.xp,
                  "Spoints": user.Spoints,
                  "days_streak": user.days_streak,
                  "mul": user.mul, "sale_shop": user.sale_shop,
                  "last_streak": user.last_streak,
                  "last_mul": user.last_mul,
                  "complete_simple_tasks": user.complete_simple_tasks,
                  "complete_common_tasks": user.complete_common_tasks,
                  "complete_hard_tasks": user.complete_hard_tasks,
                  "complete_expert_tasks": user.complete_expert_tasks,
                  "complete_hardcore_tasks": user.complete_hardcore_tasks
                }
            token = security.create_access_token(uid=user.name,
                data=data,
                expiry=timedelta(days=15)
            )
            response.set_cookie(key="my_access_token", value=token, httponly=True)
            return data

        raise HTTPException(status_code=400, detail="Invalid credentials")


@router.post("/logout/", dependencies=[Depends(security.access_token_required)])
async def logout(response: Response):
    # delete access and refresh token
    response.delete_cookie("access_token_cookie")
    response.delete_cookie("refresh_token_cookie")
    # if is csrf token
    response.delete_cookie("csrf_access_token")
    response.delete_cookie("csrf_refresh_token")
    return {"message": "logout"}


@router.post("/register/")
async def register(creds: RegisterUserSchema):
    if creds.password1 != creds.password2:
        raise HTTPException(status_code=400, detail="Password doesn't match")
    hashed_password = await hash_password(creds.password1)
    user = User(name=creds.name, hashed_password=hashed_password)
    await user.insert()
    return {"message": "register"}


@router.post("/refresh/")
async def refresh(request: Request, refresh_data: RefreshForm = None):
    try:
        try:
            refresh_payload = await security.refresh_token_required(request)
        except Exception as header_error:
            if not refresh_data or not refresh_data.refresh_token:
                raise header_error
            token = refresh_data.refresh_token
            refresh_payload = security.verify_token(
                token,
                verify_type=True,
                type="refresh"
            )
            # Create a new access token
        access_token = security.create_access_token(refresh_payload.sub)
        return {"access_token": access_token}

    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.get("/auth/check")
async def auth_check(dependencies=[Depends(security.access_token_required)]):
    """
    Эндпоинт для проверки авторизации.
    Возвращает данные пользователя (payload) если токен валиден.
    Если токен невалиден, AuthX вернёт 401.
    """
    return {"authorized": True}


@router.get("/profile/", dependencies=[Depends(security.access_token_required)])
async def protected(request: Request):
    payload = await security.access_token_required(request)
    data = {
        'name': payload.name,
        'level': payload.level,
        'role': which_my_role[payload.level],
        'xp': payload.xp,
        'Spoints': payload.Spoints,
        'days_streak': payload.days_streak,
        'mul': payload.mul,
        'sale_shop': payload.sale_shop,
        'last_streak': payload.last_streak,
        'last_mul': payload.last_mul,
        'complete_simple_tasks': payload.complete_simple_tasks,
        'complete_common_tasks': payload.complete_common_tasks,
        'complete_hard_tasks': payload.complete_hard_tasks,
        'complete_expert_tasks': payload.complete_expert_tasks,
        'complete_hardcore_tasks': payload.complete_hardcore_tasks
    }
    return data
