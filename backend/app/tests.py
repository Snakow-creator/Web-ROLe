from models.models import Task
from tasks.data import tasks_expired
from datetime import datetime

import asyncio

async def update_tasks():
    tasks = await Task.find().to_list()

    for task in tasks:
        if tasks_expired[task.type] != None:
            if (datetime.now() - task.date).days >= tasks_expired[task.type]:
                await task.update({"$set": {"inactive": True}})
