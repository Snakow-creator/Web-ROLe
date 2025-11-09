from base.config import BaseRepository
from models.models import User


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    async def get_by_name(self, name):
        return await self.find_one(User.name == name)


    async def insert_user(self, name, hashed_password):
        # create user and insert to mongodb
        user = self.model(name=name, hashed_password=hashed_password)

        await user.insert()
        return user
