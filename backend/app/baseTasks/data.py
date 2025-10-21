from baseTasks.requests import get_baseTasks

list_baseTasks = get_baseTasks()

baseTasks_data = (
    {
        "difficulty": "simple",
        "points": 20,
    },
    {
        "difficulty": "common",
        "points": 50,
    },
    {
        "difficulty": "hard",
        "points": 200,
    },
    {
        "difficulty": "expert",
        "points": 500,
    },
    {
        "difficulty": "hardcore",
        "points": 5000,
    },
)


