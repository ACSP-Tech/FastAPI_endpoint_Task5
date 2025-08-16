#importing the necessary requirement
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from note_utils import check_filepath
import json
import os

#calling a fastapi instance
app = FastAPI()

#class atributes for notes
class Note(BaseModel):
    title: str
    notes: str

#endpoint to handlle add new notes
@app.post("/notes/", status_code=status.HTTP_201_CREATED)
#route function that take it the Note attribute as a json body parameter
def add_note(data:Note):
    try:
        #os module and check_filepath() to handle sourcing note.txt from file path
        check_filepath() 
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "note.txt")
        with open(file_path, "r") as file:
            try:
                old_json = json.load(file)
            except json.JSONDecodeError:
                old_json = []  # empty file case if there is no previous notes
        #if there is a match in new title with existing title raise conflict exception
        if any(item["title"] == data.title for item in old_json):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Note with '{data.title}' title already exists, try saving again with a different title"
            )
        #else add new notes and title to txt file
        old_json.append(data.model_dump())
        with open(file_path, "w") as file:
            json.dump(old_json, file)
            #return the current addition if successful
            return data
    #handling try exceptions
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Oops! unable to process your request"
        )
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")

#endpoint to handle filter the notes based on title which is passed as a path parameter 
@app.get("/notes/{title}")
def filter_by_title(title:str):
    try:
        #os module and check_filepath() to handle sourcing note.txt from file path
        check_filepath() 
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "note.txt")
        #reading and loading json file
        with open(file_path, "r") as file:
            try:
                old_json = json.load(file)
            except json.JSONDecodeError:
                old_json = []   #empty file case if there is no previous notes
        # Find matching notes and stores it in a list
        matches = [item for item in old_json if item["title"].lower().strip() == title.lower().strip()]
        # retrun match if found 
        if matches:
            return matches
        #raise an exception if no match found
        elif matches == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Note with '{title}' title not found, try searching with a different title")
    #handling try exceptions
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")

#endpoint to handle partial update of notes(only notes fields), to complete change the notes, kindly delete it with the endpoints and create a new note (endpoints)
@app.patch("/notes/{title}")
def update_by_title(title:str, data:Note):
    try:
        #os module to handle file path sourcing
        check_filepath() 
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "note.txt")
        #reading and loading from a json file
        with open(file_path, "r") as file:
            try:
                old_json = json.load(file)
            except json.JSONDecodeError:
                old_json = []  #empty file case if there is no previous notes
        # Find the index of the matching note
        for idx, item in enumerate(old_json):
            if item["title"].lower().strip() == title.lower().strip():
                # Update only the fields provided in data
                old_json[idx]["title"] = data.title
                old_json[idx]["notes"] = data.notes
        # Save back to file
        with open(file_path, "w") as f:
            json.dump(old_json, f, indent=4)
            return data
        # If no match found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with title '{title}' not found, try updating with a different title"
        )
    #handling try exceptions
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")

#endpoints to handle delete request (don't know if I got this right though, saviour, please let me know what I can do better)
@app.delete("/notes/{title}")
def update_by_title(title:str):
    try:
        #os module and check_filepath() function to handle filepath sourcing
        check_filepath() 
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "note.txt")
        #reading and loading file
        with open(file_path, "r") as file:
            try:
                old_json = json.load(file)
            except json.JSONDecodeError:
                old_json = []  #empty file case if there is no previous notes
        # Find the index of the matching notes
        for idx, item in enumerate(old_json):
            if item["title"].lower().strip() == title.lower().strip():
                # delete only the fields provided in data
                old_json.pop(idx)
                break
        # Save back to file after deleting the matching record
        with open(file_path, "w") as f:
            json.dump(old_json, f, indent=4)
            return old_json
        # If no match found raise exception
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with title '{title}' not found, try updating with a different title"
        )
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")