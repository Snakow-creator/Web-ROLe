from fastapi import APIRouter
from routers import root
from api_demo.auth.handler import router as auth_router


init_router = APIRouter()
init_router.include_router(root.router)
init_router.include_router(auth_router)
