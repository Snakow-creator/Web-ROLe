from models.models import User
from fastapi import APIRouter, Depends
from api.core.security import security
from items.requests import get_items, buy_item


router = APIRouter(tags=['items'])


@router.get('/items', dependencies=[Depends(security.access_token_required)])
async def list_items(
    user: User = Depends(security.get_current_subject)
):
    return await get_items(user['level'], user['name'])


@router.put('/buy/item/{id}', dependencies=[Depends(security.access_token_required)])
async def handler_buy_item(
    id: str,
    user: User = Depends(security.get_current_subject
)):
    return await buy_item(id, user['name'])

