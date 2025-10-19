from fastapi import Request, Response, HTTPException
from authx.dependencies import AuthXDependency
from typing import Optional


class TokenRefresher:
    def __init__(self, auth: AuthXDependency):
        self.auth = auth

    async def refresh_token(self, request: Request = None) -> dict:
        response = response or self.auth.request

        try:
            # get current user from refresh token
            user = await self.auth.get_current_subject()
            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="no valid refresh token"
                )

            # create a new access token
            token = await self.auth.create_access_token(user)


