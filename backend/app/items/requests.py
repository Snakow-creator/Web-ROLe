from models.models import ShopItem, User

from beanie import PydanticObjectId as ObjectId


async def get_items():
    return await ShopItem.find().to_list()


async def buy_item(id, name):
    item = await ShopItem.get(ObjectId(id))
    user = await User.find_one(User.name == name)

    await user.update({
        "$inc": {
            "Spoints": -item.price * user.sale_shop
        }
    })

    return {"message": f"Вы купили {item.title} за {item.price} Spoints"}
