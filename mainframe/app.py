from fastapi import FastAPI
from pydantic import BaseModel
import main

app = FastAPI()


class Task(BaseModel):
    task: str


@app.post("/final")
async def final_endpoint(task: Task):
    print(main.Final(task.task))
    return {"response": main.Final(task.task)}
