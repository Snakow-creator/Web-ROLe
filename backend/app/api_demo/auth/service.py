from fastapi import Request
from authx import RequestToken, AuthXDependency
from typing import Callable, Awaitable
from datetime import timedelta

from api_demo.core.security import security


OptTokenGetter = Callable[[Request], Awaitable[RequestToken | None]]

get_optional_access_from_request: OptTokenGetter = security.get_token_from_request(
    type = "access",
    optional = False,
)


class TokenAuthentication:
    def __init__(self):
       self.get_optional_access_token = get_optional_access_from_request

    @staticmethod
    def authenticate_user(deps: AuthXDependency, user_id: str, data: dict):
        # 1. create tokens
        access_token = deps.create_access_token(
            uid=user_id,
            data=data,
            expiry=timedelta(seconds=600),
        )
        refresh_token = deps.create_refresh_token(uid=user_id) # refresh without data

        # 2. set cookies
        deps.set_access_cookies(token=access_token)
        deps.set_refresh_cookies(token=refresh_token)

    @staticmethod
    def logout_user(deps):
        deps.unset_access_cookies()
        deps.unset_refresh_cookies()

        return {"message": "DISCONNECTED"}

    @staticmethod
    def refresh_user(deps, request):
        return deps.refresh_token(request=request)

auth = TokenAuthentication()
