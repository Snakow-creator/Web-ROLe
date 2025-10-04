from fastapi import APIRouter, Depends, Response, HTTPException
from authx import AuthX, AuthXConfig

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

secutity = AuthX(config=config)


@router.post("/login/")
async def login(creds: UserSchema, response: Response):
    if creds.name == "test" and creds.password == "testtest":
        token = secutity.create_access_token(uid="11111",
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
            token = secutity.create_access_token(uid="111",
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


@router.get("/logout/")
async def logout():
    return {"message": "logout"}


@router.post("/register/")
async def register(creds: RegisterUserSchema):
    if creds.password1 != creds.password2:
        raise HTTPException(status_code=400, detail="Password doesn't match")
    hashed_password = await hash_password(creds.password1)
    user = User(name=creds.name, hashed_password=hashed_password)
    await user.insert()
    return {"message": "register"}



@router.get("/protected", dependencies=[Depends(secutity.access_token_required)])
async def protected():
    return
