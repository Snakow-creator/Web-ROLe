from base.config import BaseRepository
from models.models import Item


class ItemsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Item)

    async def insert_item(self, base_item, name):
        # save data item to mongodb
        item = self.model(
            title=base_item.title,
            description=base_item.description,
            price=base_item.price,
            name=name,
        )

        await item.insert()
        return item

    async def get_user_items(self, name):
        # get user buy items
        return await self.model.find(
            self.model.name == name
        ).sort(-self.model.date).to_list()


