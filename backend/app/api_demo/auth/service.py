from fastapi import Request, Response
from authx import RequestToken
from typing import Callable, Awaitable
from datetime import timedelta

from api_demo.core.security import security, name_refresh_token


OptTokenGetter = Callable[[Request], Awaitable[RequestToken | None]]

get_optional_access_from_request: OptTokenGetter = security.get_token_from_request(
    type="access",
    optional=False,
)


class TokenAuthentication:
    def __init__(self):
        self.get_optional_access_token = get_optional_access_from_request

    @staticmethod
    async def authenticate_user(response: Response, user_id: str, data: dict):
        # 1. create tokens
        access_token = security.create_access_token(
            uid=user_id,
            data=data,
            expiry=timedelta(minutes=10),
        )
        # refresh without data
        refresh_token = security.create_refresh_token(
            uid=user_id,
        )

        # 2. set cookies
        response.set_cookie(
            key=name_refresh_token,
            value=refresh_token,
            samesite="lax",
            httponly=True, # not visible to js
            secure=False, # True in production
            max_age=30*24*60*60
        )

        return {"access_token": access_token}

    @staticmethod
    def logout_user(deps):
        deps.unset_refresh_cookies()

        return {"message": "DISCONNECTED"}

    @staticmethod
    def refresh_user(deps, request):
        return deps.refresh_token(request=request)


auth = TokenAuthentication()
