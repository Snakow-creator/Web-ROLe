from models.models import User, Task
from baseTasks.data import baseTasks_points, task_bonus
from levels.hooks import current_level

from beanie import PydanticObjectId as ObjectId
from datetime import datetime, timezone


async def up_level(name, level):
    user = await User.find_one(User.name == name)

    # add points * n if up level more than 1
    points = (level - user.level) * 200

    await user.update(
        {
            "$inc": {"Spoints": points},
            "$set": {"level": level},
        }
    )

    return {"message": f"Уровень повышен, награда: +{points} Spoints", "points": points}


async def deprive_level(name, level):
    user = await User.find_one(User.name == name)

    # calculate levels
    levels = user.level - level

    # add points * n if up level more than 1
    points = (user.level - level) * 200

    await user.update(
        {
            "$inc": {"Spoints": -points},
            "$set": {"level": level},
        }
    )

    return {"message": f"Уровень понижен на {levels}", "points": points}


async def complete_task(id, name):
    # find task and user
    task = await Task.get(ObjectId(id))
    user = await User.find_one(User.name == name)
    # find active user tasks by type
    tasks = await Task.find(
        Task.user == name,
        Task.type == task.type,
        Task.completed == False,
        Task.inactive == False,
    ).to_list()

    # points for task
    points = baseTasks_points[task.type]

    # check if task is last, then add bonus task
    if len(tasks) == 1:
        points = points * task_bonus

    # update last_streak if needed
    if user.last_streak != datetime.now().strftime("%Y-%m-%d"):
        await user.update(
            {
                "$set": {
                    "last_streak": datetime.now(timezone.utc).strftime("%Y-%m-%d")
                },
                "$inc": {"days_streak": 1},
            }
        )

    # update user points
    await user.update(
        {"$inc": {
            "Spoints": points,
            "xp": points,
            f"complete_{task.type}_tasks": 1,
        }}
    )

    # task update, do task is inactive
    await task.update(
        {"$set": {
            "completed": True,
            "complete_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "awarded_points": points
        }}
    )

    # update level if current level higher than task level
    level = current_level(user.xp)
    if level > user.level:
        res = await up_level(name, level)
        print(res)
        return {
            "message": "Task completed",
            "up_level": True,
            "points": points,
            "xp": points,
            "spoints_level": res["points"],
        }

    return {"message": "Task completed", "up_level": False, "points": points, "xp": points}


async def uncomplete_task(id, name):
    # find task and user
    task = await Task.get(ObjectId(id))
    user = await User.find_one(User.name == name)

    points = task.awarded_points

    # task update, do task is active
    await task.update(
        {"$set": {
            "completed": False,
            "complete_date": None,
            "awarded_points": 0
        }}
    )

    # deprive user points
    await user.update(
        {"$inc": {
            "Spoints": -points,
            "xp": -points,
            f"complete_{task.type}_tasks": -1,
        }}
    )

    # update level if current level less than user level
    level = await current_level(user.xp)
    if user.level > level:
        res = await deprive_level(name, level)
        print(res)

    return {"message": "Task uncompleted", "points": points, "xp": points}
