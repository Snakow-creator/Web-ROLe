from models.models import ShopItem
from items.data import items_data

async def load_items():
    for item in items_data:
        if await ShopItem.find_one(ShopItem.title == item["title"]):
            continue
        await ShopItem.insert_one(item)
