from models.models import Task
from tasks.data import tasks_expired

from datetime import datetime, timezone

import logging



async def update_tasks():
    tasks = await Task.find_all().to_list()

    for task in tasks:
        if tasks_expired[task.type] != None:
            if (datetime.utcnow() - task.date).days >= tasks_expired[task.type]:
                await task.update({"$set": {"inactive": True}})
