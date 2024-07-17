from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

'''
    pydantic model used as Data Validator
'''
class Student(BaseModel):
    id: str
    name : str
    gender: str
    age: int

db = [Student(id='0001', name="Alice", gender="Female", age=20)]

app = FastAPI()

@app.post('/add_student')
async def add_student(student: Student):
    db.append(student)
    return student

@app.get('/get_student/{student_id}')
async def get_student( student_id : str ):
    for s in db:
        if s.id == student_id:
            return s
    raise HTTPException(status_code= 404, detail='Student not found')
