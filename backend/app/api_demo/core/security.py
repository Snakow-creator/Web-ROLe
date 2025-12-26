from pydantic import BaseModel
from authx import AuthX, AuthXConfig

from models.models import User
from models.settings import settings
from database.core import role_db


users = role_db["users"]

config = AuthXConfig(
    JWT_SECRET_KEY=settings.jwt_secret,
    JWT_ALGORITHM="HS256",
    JWT_ACCESS_COOKIE_NAME="my_access_token",
    JWT_REFRESH_COOKIE_NAME="my_refresh_token",
    JWT_TOKEN_LOCATION=["headers", "query", "cookies", "json"],
)



name_access_token = config.JWT_ACCESS_COOKIE_NAME
name_refresh_token = config.JWT_REFRESH_COOKIE_NAME
name_csrf_token = config.JWT_ACCESS_CSRF_COOKIE_NAME

security = AuthX(
    config=config,
    model=User,
)


class RefreshForm(BaseModel):
    refresh_token: str


# create query in mongodb
@security.set_subject_getter
def get_user_from_uid(uid: str) -> User:
    user = users.find_one({"name": uid})
    print("UID FROM TOKEN:", repr(uid), user)
    return user
