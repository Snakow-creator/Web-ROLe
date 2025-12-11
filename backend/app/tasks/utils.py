from repositories import task_repo, user_repo
from models.models import User

from tasks.data import tasks_expired

from datetime import datetime, timezone


async def update_tasks():
    tasks = await task_repo.find_all()

    for task in tasks:
        if tasks_expired[task.type] != None:
            if (datetime.utcnow() - task.date).days >= tasks_expired[task.type]:
                await task.update({"$set": {"inactive": True}})




async def weekly_bonus(user: User):
    # get time
    time_now = datetime.now(timezone.utc),
    await user.update({
        "$inc": {"Spoints": 150, "xp": 150},
        "$set": {
            "last_mul": time_now,
            "mul": user.mul * 1.02, # x 2 % bonus
            "sale_shop": user.sale_shop * 0.985 # * 1 % sale bonus
        }
    })

