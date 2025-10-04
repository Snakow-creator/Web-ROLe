from fastapi import APIRouter, Depends, Response, HTTPException, Request
from authx import AuthX, AuthXConfig
from pydantic import BaseModel

from models.models import User
from models.schemas import UserSchema, RegisterUserSchema
from api_demo.auth.crypt import hash_password, verify_password

from datetime import datetime, timedelta

router = APIRouter(tags=["auth"])

config = AuthXConfig()
config.JWT_SECRET_KEY = "MY_SECRET_KEY"
config.JWT_ALGORITHM = "HS256"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)


class RefreshForm(BaseModel):
    refresh_token: str


@router.post("/login/")
async def login(creds: UserSchema, response: Response):
    if creds.name == "test" and creds.password == "testtest":
        token = security.create_access_token(uid="11111",
            data={"name": "test",
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
            },
            expiry=timedelta(days=15)
        )
        response.set_cookie(key="my_access_token", value=token, httponly=True)
        return {"access_token": token, "token_type": "test"}
    else:
        user = await User.find_one(User.name == creds.name)
        if await verify_password(creds.password, user.hashed_password):
            token = security.create_access_token(uid=user.name,
                data={"name": user.name,
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
                },
                expiry=timedelta(days=15)
            )
            response.set_cookie(key="my_access_token", value=token, httponly=True)
            return {"access_token": token, "token_type": "user"}

        raise HTTPException(status_code=400, detail="Invalid credentials")


@router.post("/logout/", dependencies=[Depends(security.access_token_required)])
async def logout():
    security.unset_access_cookies()
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


@router.get("/profile", dependencies=[Depends(security.access_token_required)])
async def protected():
    return
