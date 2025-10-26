from fastapi import APIRouter, HTTPException, Depends, Request

from models.schemas import TaskSchema
from models.models import Task, User
from baseTasks.data import list_baseTasks
from api_demo.core.security import security

router = APIRouter(tags=["tasks"])


@router.get("/tasks", dependencies=[Depends(security.access_token_required)])
async def tasks(
    user: User = Depends(security.get_current_subject),
):
    tasks = await Task.find(Task.user == user['name']).sort(-Task.date).to_list()
    return tasks


@router.post("/add/task", dependencies=[Depends(security.access_token_required)])
async def add_task(
    creds: TaskSchema,
    user: User = Depends(security.get_current_subject),
):
    if creds.type not in list_baseTasks:
        raise HTTPException(status_code=400, detail="Invalid task type")
    task = Task(
       title=creds.title,
       description=creds.description,
       type=creds.type,
       user=user["name"]
    )
    await task.insert()
    return {"message": "Task added"}
