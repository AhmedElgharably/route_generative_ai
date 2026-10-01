from dataclasses import asdict

from fastapi import FastAPI, HTTPException

from models import Task
from schemas import TaskCreate, TaskResponse, TaskUpdate

app = FastAPI(title="Task Management API")
tasks: dict[int, Task] = {}




@app.post("/tasks", response_model=TaskResponse)
def create_task(task_in: TaskCreate):
    data = task_in.model_dump()                 
    task_id = len(tasks) + 1                    
    task = Task(task_id=task_id, **data)        
    tasks[task_id] = task
    return TaskResponse(**asdict(task))         







@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks():
    return [TaskResponse(**asdict(task)) for task in tasks.values()]





@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return {"message": f"Task {task_id} deleted successfully"}





@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    updates = task_update.model_dump(exclude_unset=True, exclude_none=True)
    existing = asdict(tasks[task_id])
    new_task = Task(**{**existing, **updates})  
    tasks[task_id] = new_task
    return TaskResponse(**asdict(new_task))
