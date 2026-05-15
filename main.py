import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

tasks = [
    {
        "id":1,
        "title": "Learn API",
        "description": None,
        "is_completed": False,
    },
{
        "id":2,
        "title": "Make a program",
        "description": None,
        "is_completed": False,
    }
]
@app.get(
    "/tasks",
    tags=["Задачи"],
    summary="Получить все задачи",
)
def read_tasks():
    return tasks

@app.get(
    "/tasks/{task_id}",
    tags=["Задачи"],
    summary="Получить конкретную задачу",
)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="404 Not found")

class NewTask(BaseModel):
    title: str
    description: str | None
    # is_completed: bool = Field(False)

@app.post("/tasks", tags=["Задачи"])
def create_new_task(new_task: NewTask):
    tasks.append({
        "id":len(tasks)+1,
        "title": new_task.title,
        "description": new_task.description,
        "is_completed": False
    })
    return {"success":True, "message":"Задача успешно добавлена"}


class UpdateTask(BaseModel):
    title: str
    description: str | None
    is_completed: bool
@app.put(
    "/tasks/{task_id}",
    tags=["Задачи"],
    summary="Обновить задачу"
)
def update_tasks(task_id: int, update_task: UpdateTask):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = update_task.title
            task["description"] = update_task.description
            task["is_completed"] = update_task.is_completed
            return {
                "success": True,
                "message": "Задача обновлена",
                "task": task
            }
    raise HTTPException(status_code=404, detail="404 Not found")

@app.delete(
    "/tasks/{task_id}",
    tags=["Задачи"],
    summary="Удалить конкретную задачу",
)
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"success": True, "message": "Задача успешно удалена"}
    raise HTTPException(status_code=404, detail="404 Not found")


if __name__=="__main__":
    uvicorn.run("main:app", reload=True)