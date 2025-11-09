from repositories import user_repo, shop_items_repo, items_repo


async def get_items(level):
    return await shop_items_repo.get_by_min_level(level)


async def buy_item(id, name):
    item = await shop_items_repo.get(id)
    user = await user_repo.get_by_name(name)

    await user.update({
        "$inc": {
            "Spoints": -item.price * user.sale_shop
        }
    })

    # insert buy item in db
    await items_repo.insert_item(item, name)

    return {"message": f"Вы купили \"{item.title}\" за {item.price} Spoints"}
