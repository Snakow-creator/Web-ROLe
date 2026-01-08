from fastapi import Request, Response
from fastapi.responses import JSONResponse
from authx import RequestToken
from authx.exceptions import JWTDecodeError
from typing import Callable, Awaitable
from datetime import timedelta

from api_demo.core.security import security


OptTokenGetter = Callable[[Request], Awaitable[RequestToken | None]]

get_optional_access_from_request: OptTokenGetter = security.get_token_from_request(
    type="access",
    optional=False,
)


class TokenAuthentication:
    def __init__(self):
        self.get_optional_access_token = get_optional_access_from_request

    @staticmethod
    async def authenticate_user(user_id: str, data: dict):
        # 1. create tokens
        access_token = security.create_access_token(
            uid=user_id,
            data=data,
            expiry=timedelta(days=14),
        )

        return {"access_token": access_token}

    @staticmethod
    def logout_user(deps):
        deps.unset_refresh_cookies()

        return {"message": "DISCONNECTED"}

    @staticmethod
    async def safe_access_token_getter(request: Request):
        token_getter = security.get_token_from_request(
            type="access", optional=True
        )
        try:
            payload = await token_getter(request)
            security.verify_token(
                payload, verify_type=True, verify_csrf=False
            )
            return payload
        except JWTDecodeError as ex:
            # token is expired
            if "Signature has expired" in str(ex):
                return JSONResponse(
                    status_code=401,
                    content={"message": "EXPIRED", "auth": False, "expire": True},
                )
            # token is invalid
            return JSONResponse(
                status_code=401,
                content={"message": "UNAUTHORIZED", "auth": False, "expire": False},
            )



auth = TokenAuthentication()
