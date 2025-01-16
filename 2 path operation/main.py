from fastapi import FastAPI, Path
from typing import Optional
'''
GET : retrieve 
POST : create 
PUT : update
DELETE : delete
'''
app = FastAPI()

@app.get('/')
async def root():
    return 'Hello World'

students = {
    1: {
        "name": "Nguyen Tien Trong",
        "age": 21,
        "sex": "male"
    },
    2: {
        "name": "Nguyen Tien Long",
        "age": 21,
        "sex": "Female"
    }
}

# Path parameter
@app.get('/get_student/{student_id}')
async def get_student(student_id: int = Path(..., description='The ID of the student you want to view', gt=0 , lt=3)):
    return students[student_id]

# Query parameter
@app.get('/get_student_by_name/')
async def get_student( name: Optional[str] = None):
    for student_id in students:
        if students[student_id]['name'] == name:
            return students[student_id]
    return {'Data': 'Not Found'}

# combine path and query parameter
@app.get('/get_student/{student_id}/')
async def get_student(student_id: int = Path(..., description='The ID of the student you want to view', gt=0 , lt=3), name: Optional[str] = None):
    if name:
        for student_id in students:
            if students[student_id]['name'] == name:
                return students[student_id]
        return {'Data': 'Not Found'}
    return students[student_id]

# POST method

from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
    sex : str

@app.post('/create_student/{student_id}')
async def create_student( student_id: int, student: Student ):
    if student_id in students:
        return {'Error': 'Student already exists'}
    students[student_id] = student
    return students[student_id]