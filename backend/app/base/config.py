from beanie import PydanticObjectId as ObjectId


class BaseRepository:
    def __init__(self, model):
        # get model by beanie
        self.model = model

    async def get(self, _id):
        # return object by mongodb id
        # _id = mongodb object id

        return await self.model.get(ObjectId(_id))

    async def find_one(self, query):
        # find one object by query
        # query must be a boolean beanie query
        # for example: model.name == "name"

        return await self.model.find_one(query)

    async def find_all(self, query=None):
        # find all objects by query
        # query must be a boolean beanie query
        # for example: model.name == "name"

        if query:
            return await self.model.find_all(query).to_list()
        else:
            return await self.model.find_all().to_list()
