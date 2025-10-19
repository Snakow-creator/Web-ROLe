from fastapi import Request
from authx import RequestToken
from typing import Callable, Awaitable

from api_demo.core.security import security


OptTokenGetter = Callable[[Request], Awaitable[RequestToken | None]]

get_optional_access_from_request: OptTokenGetter = security.get_token_from_request(
        type = "access",
        optional = True,
    )


class TokenAuthentication:
    def __init__(self):
       self.get_optional_access_token = get_optional_access_from_request

    @staticmethod
    def authenticate_user(deps, user_id, data):
        # 1. create tokens
        access_token = deps.create_access_token(uid=user_id, data=data)
        refresh_token = deps.create_refresh_token(uid=user_id, data=data)

        # 2. set cookies
        deps.set_access_cookies(token=access_token)
        deps.set_refresh_cookies(token=refresh_token)

    @staticmethod
    def logout_user(deps):
        deps.unset_access_cookies()
        deps.unset_refresh_cookies()

        return {"message": "DISCONNECTED"}

auth = TokenAuthentication()
