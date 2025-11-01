from fastapi import APIRouter, Depends
from models.models import User
from api_demo.core.security import security
from items.requests import get_items, buy_item


router = APIRouter(tags=['items'])


@router.get('/items', dependencies=[Depends(security.access_token_required)])
async def list_items():
    return await get_items()


@router.post('/buy/item/{id}', dependencies=[Depends(security.access_token_required)])
async def handler_buy_item(
    id: str,
    user: User = Depends(security.get_current_subject
)):
    return await buy_item(id, user['name'])

