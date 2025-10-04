from models.models import BaseTask
from baseTasks.data import baseTasks_data

async def load_baseTasks():
    for task in baseTasks_data:
        if await BaseTask.find_one(BaseTask.difficulty == task["difficulty"]):
            continue
        await BaseTask.insert_one(task)


