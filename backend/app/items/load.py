from models.models import ShopItem
from items.data import items_data

async def load_items():
    for item in items_data:
        if await ShopItem.find_one(ShopItem.title == item["title"]):
            continue
        item_obj = ShopItem(
            title=item["title"],
            description=item["description"],
            price=item["price"],
            type=item["type"],
            min_level=item["min_level"],
        )
        await ShopItem.insert_one(item_obj)
