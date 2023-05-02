from fastapi import BackgroundTasks, FastAPI
from typing import Optional
from pydantic import BaseModel
import time
import asyncio



app = FastAPI()



@app.get("/")
def root():
  return {"message": "Hello World"}



@app.get("/courses/{course_name}")
def read_course(course_name: int):
    return {"course_name": course_name}



course_items = [
   {"course_name": "Python"}, 
   {"course_name": "NodeJS"}, 
   {"course_name": "Machine Learning"}]

# @app.get("/courses/")
# def read_courses(start = 0, end = 100):
#     return course_items[start : start + end]



course_it = {1: "Python", 2: "NodeJS", 3: "Machine Learning"}

@app.get("/courses/{course_id}")
def read_courses(course_id: int, q: Optional[str] = None):
    if q is not None:
        return {"course_name": course_it[course_id], "q": q} 
    return {"course_name": course_it[course_id]}



class Course(BaseModel):
    name: str
    description: Optional[str] = None
    price: int
    author: Optional[str] = None

@app.post("/courses/")
def create_course(course: Course):
    return course



def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)

@app.post("/send-notification/{email}")
def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}



@app.get("/async")
async def home():
    tasks = []
    start = time.time()
    for i in range(2):
        tasks.append(asyncio.create_task(func1()))
        tasks.append(asyncio.create_task(func2()))
    response = await asyncio.gather(*tasks)
    end = time.time()
    return {"response": response, "time_taken": (end - start)}

async def func1():
    await asyncio.sleep(2)
    return "Func1() Completed"

async def func2():
    await asyncio.sleep(1)
    return "Func2() Completed"

#uvicorn main:app --reload