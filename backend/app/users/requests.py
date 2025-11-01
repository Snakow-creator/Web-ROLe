from models.models import User, Task
from baseTasks.data import baseTasks_points
from levels.hooks import current_level

from beanie import PydanticObjectId as ObjectId
from datetime import datetime


async def up_level(name, level):
    user = await User.find_one(User.name == name)

    # add points * n if up level more than 1
    points = (level - user.level) * 200

    await user.update({
        "$inc": {"Spoints": points},
        "$set": {"level": level},
    })

    return {"message": f"Level up, +{points} points"}


async def complete_task(id, name):
    # find task and user
    task = await Task.get(ObjectId(id))
    user = await User.find_one(User.name == name)

    # points for task
    points = baseTasks_points[task.type]

    # update last_streak if needed
    if user.last_streak != datetime.now().strftime("%Y-%m-%d"):
        await user.update({
            "$set": {"last_streak": datetime.now().strftime("%Y-%m-%d")},
            "$inc": {"days_streak": 1}
        })

    # update user points
    await user.update({
        "$inc": {
            "Spoints": points,
            "xp": points
        }
    })

    # delete task
    await task.delete()

    # update level if current level higher than task level
    level = current_level(user.xp)
    if level > user.level:
        await up_level(name, level)
        return {"message": "Task completed", "up_level": True}

    return {"message": "Task completed", "up_level": False}


