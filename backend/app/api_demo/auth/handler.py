from fastapi import (APIRouter, Depends, HTTPException, Request)
from authx import AuthXDependency
from datetime import datetime

from api_demo.auth.crypt import hash_password, verify_password
from api_demo.auth.service import auth
from api_demo.core.config import test_data
from api_demo.core.security import security, RefreshForm

from models.models import User
from models.schemas import UserSchema, RegisterUserSchema
from levels.data import which_my_role


router = APIRouter(tags=["auth"])


@router.post("/login")
async def login(
    creds: UserSchema,
    deps: AuthXDependency = Depends(security.get_dependency)
):
    if creds.name == "test" and creds.password == "testtest":
        user_id = "test"
        data = {**test_data}
    else:
        user = await User.find_one(User.name == creds.name)
        if await verify_password(creds.password, user.hashed_password):
            user_id = user.name
            data = {"name": user.name,
                  "level": user.level,
                  "xp": user.xp,
                  "Spoints": user.Spoints,
                  "days_streak": user.days_streak,
                  "mul": user.mul, "sale_shop": user.sale_shop,
                  "last_streak": user.last_streak.timestamp(),
                  "last_mul": user.last_mul.timestamp(),
                  "complete_simple_tasks": user.complete_simple_tasks,
                  "complete_common_tasks": user.complete_common_tasks,
                  "complete_hard_tasks": user.complete_hard_tasks,
                  "complete_expert_tasks": user.complete_expert_tasks,
                  "complete_hardcore_tasks": user.complete_hardcore_tasks
                }
    auth.authenticate_user(deps, user_id, data)
    return data


@router.post('/logout', dependencies=[Depends(security.get_dependency)])
async def logout(
    deps: AuthXDependency = Depends(security.get_dependency)
):
    return auth.logout_user(deps)


@router.post("/register")
async def register(creds: RegisterUserSchema):
    if creds.password1 != creds.password2:
        raise HTTPException(status_code=400, detail="Password doesn't match")
    hashed_password = await hash_password(creds.password1)
    user = User(name=creds.name, hashed_password=hashed_password)
    await user.insert()
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
                token,
                verify_type=True,
                type="refresh"
            )
            # Create a new access token
        access_token = security.create_access_token(refresh_payload.sub)
        return {"access_token": access_token}

    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.get('/protected')
def protected(user = Depends(auth.get_optional_access_token)):
    if user:
        return {"message": "AUTHORIZED", "auth": True}
    else:
        return {"message": "NOT AUTHORIZED", "auth": False}



@router.get("/profile", dependencies=[Depends(security.access_token_required)])
async def profile(
    user: User = Depends(security.get_current_subject),
):
    try:
        data = {
            'name': user['name'],
            'level': user['level'],
            'role': which_my_role.get(user['level'], 'Бог'),
            'xp': user['xp'],
            'Spoints': user['Spoints'],
            'days_streak': user['days_streak'],
            'mul': user['mul'],
            'sale_shop': user['sale_shop'],
            'last_streak': user['last_streak'],
            'last_mul': user['last_mul'],
            'complete_simple_tasks': user['complete_simple_tasks'],
            'complete_common_tasks': user['complete_common_tasks'],
            'complete_hard_tasks': user['complete_hard_tasks'],
            'complete_expert_tasks': user['complete_expert_tasks'],
            'complete_hardcore_tasks': user['complete_hardcore_tasks']
        }
        return data
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=404, detail="Not authorized")
