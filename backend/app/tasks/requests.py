from users.requests import edit_points, up_streak, edit_level
from levels.hooks import current_level
from repositories import task_repo, user_repo

from tasks.data import tasks_expired
from baseTasks.data import baseTasks_points, task_bonus

from datetime import datetime, timezone


async def update_tasks():
    tasks = await task_repo.find_all()

    for task in tasks:
        if tasks_expired[task.type] != None:
            if (datetime.utcnow() - task.date).days >= tasks_expired[task.type]:
                await task.update({"$set": {"inactive": True}})


async def complete_task(id, name):
    # find task and user
    task = await task_repo.get(id)
    user = await user_repo.get_by_name(name)
    # find active user tasks by type
    tasks = await task_repo.get_user_tasks_by_type(name, task.type)

    # points for task
    points = baseTasks_points[task.type]

    # check if task is last, then add bonus task
    if len(tasks) == 1:
        points = points * task_bonus

    # update last_streak if needed
    last_streak = user.last_streak.strftime("%Y-%m-%d")
    if last_streak != datetime.now().strftime("%Y-%m-%d"):
        await up_streak(user)

    # update user points
    await edit_points(user, points, task.type)

    # task update, do task is inactive
    await task.update(
        {"$set": {
            "completed": True,
            "complete_date": datetime.now(timezone.utc),
            "awarded_points": points
        }}
    )

    # update level if current level higher than task level
    level = current_level(user.xp)
    if level > user.level:
        res = await edit_level(name, level)
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
    task = await task_repo.get(id)
    user = await user_repo.get_by_name(name)

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
    await edit_points(user, points, task.type, -1)


    # update level if current level less than user level
    level = current_level(user.xp)
    if user.level > level:
        await edit_level(name, level)

    return {"message": "Task uncompleted", "points": points, "xp": points}
