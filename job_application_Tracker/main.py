from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from file_handler import check_filepath
import json
import os

#calling a fastapi instance
app = FastAPI()

#body class atribute required for the job application model
class JobApplication(BaseModel):
    name: str
    company: str
    position: str
    status: str

#Endpoints for adding new job application
@app.post("/applications/", status_code=status.HTTP_201_CREATED)
def add_appplication(data:JobApplication):
    try:
        #os module handling file path sourcing
        check_filepath() 
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "applications.json")
        #reading and loading json file
        with open(file_path, "r") as file:
            old_json = json.load(file)
        #converting the class data to dict and appending to previous record
        old_json.append(data.model_dump())
        #updating the json file
        with open(file_path, "w") as file:
            json.dump(old_json, file)
    #handling try exception for valueError
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Oops! unable to process your request"
        )
    #handling all other exception
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")
    #return data if try run successful
    return data

#endpoint for viewing alll aplications    
@app.get("/applications/", status_code=status.HTTP_200_OK)
def view_db():
    try:
        #os module handling file path sourcing
        check_filepath()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "applications.json")
        #reading and loading json file
        with open(file_path, "r") as file:
            old_json = json.load(file)
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")
    #return the all the job applications
    return old_json

 

#endpoint for filtering application by status
@app.get("/applications/search", status_code=status.HTTP_200_OK)
#route function to filter job application based on the query parameter status
def filter_db(status:str):
    try:
        #os module handling file path sourcing
        check_filepath()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "applications.json")
        #reading and loading json file
        with open(file_path, "r") as file:
            old_json = json.load(file)
        #case - insensititive filter match
        job_record = [record for record in old_json if record["status"].lower() == status.lower()]
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unexpected error: {e}")
    #returning matching records
    return job_record



