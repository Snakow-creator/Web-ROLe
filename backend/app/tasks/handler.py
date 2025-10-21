from fastapi import APIRouter, HTTPException, Depends

from models.schemas import TaskSchema
from models.models import Task, User
from baseTasks.data import list_baseTasks
from api_demo.auth.handler import security

router = APIRouter(tags=["tasks"])


@router.get("/tasks")
async def tasks():
    tasks = await Task.find().sort(-Task.date).to_list()
    return tasks


@router.post("/add/task")
async def add_task(
   creds: TaskSchema,
  #  user: User = Depends(security.get_current_subject)
   ):
    if creds.type not in list_baseTasks:
        raise HTTPException(status_code=400, detail="Invalid task type")
    task = Task(
       title=creds.title,
       description=creds.description,
       type=creds.type,
       user="Mark"
    )
    await task.insert()
    return {"message": "Task added"}


