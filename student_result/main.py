#importing the necessary requirements
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from students_utils import check_filepath,compute_grade
import json
import os

#calling a fastapi instance
app = FastAPI()

#student class attribute for the body parameter input
class Student(BaseModel):
    name: str
    subject_scores: float
    average: float

#student class attribute for the body parameter for the response_model
class StudentOut(BaseModel):
    name: str
    subject_scores: float
    average: float
    grade: str

#endpoints for sending new student result data to the server, return new student data with grade
@app.post("/students/",  response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def add_student(data:Student):
    try:
        #os module to handle filepath sourcing and creation if not exist
        check_filepath() 
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "student_result.json")
        #reading and loading json file
        with open(file_path, "r") as file:
            old_json = json.load(file)
        # Calculate grade based on student scores and average score
        total = data.average * 2
        grade_score = (data.subject_scores/total) * 100
        grade = compute_grade(grade_score)
        #calling the response model in order to assign grade output 
        student_out = StudentOut(
            name=data.name,
            subject_scores=data.subject_scores,
            average=data.average,
            grade=grade
        )
        #updating the student results server
        old_json.append(student_out.model_dump())
        with open(file_path, "w") as file:
            json.dump(old_json, file)
        #returning the new update
        return student_out
    #handling try exceptions
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Ensure subject_scores and average are floats"
        )
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")

#endpoints to fetch all student result data based on name path paramater, more like search by name   
@app.get("/students/{name}")
def filter_db(name:str):
    try:
        #os module and check_filepath() function to handle sourcing for filepath
        check_filepath()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "student_result.json")
        #reading and loading the all current records
        with open(file_path, "r") as file:
            old_json = json.load(file)
        #case - insensititive match with name parameter and storing the result to a record list
        student_record = [student for student in old_json if student["name"].lower() == name.lower()]
    #handle try exceptions
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student name not found/ does not exist")
    #return the matching records
    return student_record

#endpoints to display all available student record
@app.get("/students/")
def view_db():
    try:
        #os module and check_filepath() to handle filepath sourcing
        check_filepath()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "student_result.json")
        #reading and loading the file of all available student result records
        with open(file_path, "r") as file:
            old_json = json.load(file)
    #handling try exceptions 
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student name not found/ does not exist")
    #returing all student records
    return old_json

