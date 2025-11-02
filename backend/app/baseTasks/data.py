from baseTasks.requests import get_baseTasks

list_baseTasks = get_baseTasks()

task_bonus = 1.5  # + 50% of points

baseTasks_points = {
    "simple": 20,
    "common": 50,
    "hard": 200,
    "expert": 500,
    "hardcore": 5000,
}
