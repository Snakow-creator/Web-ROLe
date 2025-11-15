from fastapi import APIRouter, Depends, HTTPException, Request
from authx import AuthXDependency, RequestToken
from authx.exceptions import JWTDecodeError
from typing import Optional

from api_demo.auth.crypt import hash_password, verify_password
from api_demo.auth.service import auth
from api_demo.core.config import test_data
from api_demo.core.security import security, RefreshForm

from models.models import User
from models.schemas import UserSchema, RegisterUserSchema
from repositories import user_repo
from levels.data import which_my_role

import logging


router = APIRouter(tags=["auth"])


@router.post("/login")
async def login(
    creds: UserSchema, deps: AuthXDependency = Depends(security.get_dependency)
):
    if creds.name == "test" and creds.password == "testtest":
        user_id = "test"
        data = {**test_data}
    else:
        user = await user_repo.get_by_name(creds.name)
        if await verify_password(creds.password, user.hashed_password):
            user_id = user.name
            data = {
                "name": user.name,
                "level": user.level,
                "xp": user.xp,
                "Spoints": user.Spoints,
                "days_streak": user.days_streak,
                "mul": user.mul,
                "sale_shop": user.sale_shop,
                "last_streak": user.last_streak.timestamp(),
                "last_mul": user.last_mul.timestamp(),
                "complete_simple_tasks": user.complete_simple_tasks,
                "complete_common_tasks": user.complete_common_tasks,
                "complete_hard_tasks": user.complete_hard_tasks,
                "complete_expert_tasks": user.complete_expert_tasks,
                "complete_hardcore_tasks": user.complete_hardcore_tasks,
            }
    auth.authenticate_user(deps, user_id, data)
    return data


@router.post("/logout", dependencies=[Depends(security.get_dependency)])
async def logout(deps: AuthXDependency = Depends(security.get_dependency)):
    return auth.logout_user(deps)


@router.post("/register")
async def register(creds: RegisterUserSchema):
    if creds.password1 != creds.password2:
        raise HTTPException(status_code=400, detail="Password doesn't match")

    hashed_password = await hash_password(creds.password1)
    await user_repo.insert_user(creds.name, hashed_password)

    return {"message": "register"}


@router.post("/refresh")
async def refresh(
    request: Request,
    refresh_data: RefreshForm = None,
):
    try:
        try:
            refresh_payload = await security.refresh_token_required(request)
        except Exception as header_error:
            if not refresh_data or not refresh_data.refresh_token:
                raise header_error
            token = refresh_data.refresh_token
            refresh_payload = security.verify_token(
                token, verify_type=True, type="refresh"
            )
            # Create a new access token
        access_token = security.create_access_token(
            uid=refresh_payload.sub, data=refresh_payload.data
        )
        return {"access_token": access_token}

    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/protected")
async def protected(request: Request):
    # Check if token is valid:

    # - auth = True - if token is valid
    # - expire = True - if token is expired
    # - auth = False, expire = False - token don't found

    try:
        token_getter = security.get_token_from_request(type="access", optional=False)
        token = await token_getter(request)

        logging.warning(token)

        user = security.verify_token(token, verify_type=True)
        logging.warning(user)

        return {"message": "AUTHORIZED", "auth": True, "expire": False}

    except JWTDecodeError as ex:
        # токен истёк или повреждён
        if "Signature has expired" in str(ex):
            return {"message": "EXPIRED", "auth": False, "expire": True}
        return {"message": "UNAUTHORIZED", "auth": False, "expire": False}

    except Exception as ex:
        # токен отсутствует, невалиден, повреждён и т.д.
        return {"message": "UNAUTHORIZED", "auth": False, "expire": False}


@router.get("/profile", dependencies=[Depends(security.access_token_required)])
async def profile(
    user: User = Depends(security.get_current_subject),
):
    try:
        data = {
            "name": user["name"],
            "level": user["level"],
            "role": which_my_role.get(user["level"], "Бог"),
            "xp": user["xp"],
            "Spoints": user["Spoints"],
            "days_streak": user["days_streak"],
            "mul": user["mul"],
            "sale_shop": user["sale_shop"],
            "last_streak": user["last_streak"],
            "last_mul": user["last_mul"],
            "complete_simple_tasks": user["complete_simple_tasks"],
            "complete_common_tasks": user["complete_common_tasks"],
            "complete_hard_tasks": user["complete_hard_tasks"],
            "complete_expert_tasks": user["complete_expert_tasks"],
            "complete_hardcore_tasks": user["complete_hardcore_tasks"],
        }
        return data
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=404, detail="Not authorized")
