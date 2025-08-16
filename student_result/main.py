from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from students_utils import check_filepath,compute_grade
import json
import os

app = FastAPI()

# name = "placeholder"
# subject_scores = 0.0
# average = 0.0

#post request for adding students
class Student(BaseModel):
    name: str
    subject_scores: float
    average: float


class StudentOut(BaseModel):
    name: str
    subject_scores: float
    average: float
    grade: str

@app.post("/students/",  response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def add_student(data:Student):
    try:
        check_filepath() 
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "student_result.json")
        with open(file_path, "r") as file:
            old_json = json.load(file)
        # Calculate grade based on score
        total = data.average * 2
        grade_score = (data.subject_scores/total) * 100
        grade = compute_grade(grade_score)
        student_out = StudentOut(
            name=data.name,
            subject_scores=data.subject_scores,
            average=data.average,
            grade=grade
        )
        old_json.append(student_out.model_dump())
        with open(file_path, "w") as file:
            json.dump(old_json, file)
        return student_out
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Ensure subject_scores and average are floats"
        )
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")
    
@app.get("/students/{name}")
def filter_db(name:str):
    try:
        check_filepath()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "student_result.json")
        with open(file_path, "r") as file:
            old_json = json.load(file)
        #case - insensititive match
        student_record = [student for student in old_json if student["name"].lower() == name.lower()]
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student name not found/ does not exist")
    return student_record

@app.get("/students/")
def view_db():
    try:
        check_filepath()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "student_result.json")
        with open(file_path, "r") as file:
            old_json = json.load(file)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student name not found/ does not exist")
    return old_json

