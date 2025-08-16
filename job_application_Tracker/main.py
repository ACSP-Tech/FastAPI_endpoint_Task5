from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from file_handler import check_filepath
import json
import os

app = FastAPI()


class JobApplication(BaseModel):
    name: str
    company: str
    position: str
    status: str

@app.post("/applications/", status_code=status.HTTP_201_CREATED)
def add_student(data:JobApplication):
    try:
        check_filepath() 
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "applications.json")
        with open(file_path, "r") as file:
            old_json = json.load(file)
        old_json.append(data.model_dump())
        with open(file_path, "w") as file:
            json.dump(old_json, file)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Oops! unable to process your request"
        )
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")
    return data
    
@app.get("/applications/", status_code=status.HTTP_200_OK)
def view_db():
    try:
        check_filepath()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "applications.json")
        with open(file_path, "r") as file:
            old_json = json.load(file)
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")
    return old_json

 

@app.get("/applications/search", status_code=status.HTTP_200_OK)
def filter_db(status:str):
    try:
        check_filepath()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "applications.json")
        with open(file_path, "r") as file:
            old_json = json.load(file)
        #case - insensititive match
        job_record = [record for record in old_json if record["status"].lower() == status.lower()]
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unexpected error: {e}")
    return job_record



