from models.models import User, BaseTask

async def drop_tests_collection():
    await User.delete_all()

