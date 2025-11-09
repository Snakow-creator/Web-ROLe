from models.models import ShopItem
from base.config import BaseRepository


class ShopItemsRepository(BaseRepository):
    def __init__(self):
        super().__init__(ShopItem)

    async def get_by_min_level(self, min_level):
        return await self.model.find(ShopItem.min_level <= min_level).to_list()

