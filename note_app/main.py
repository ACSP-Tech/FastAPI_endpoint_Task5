from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from note_utils import check_filepath
import json
import os

app = FastAPI()


class Note(BaseModel):
    title: str
    notes: str

@app.post("/notes/", status_code=status.HTTP_201_CREATED)
def add_note(data:Note):
    try:
        check_filepath() 
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "note.txt")
        with open(file_path, "r") as file:
            try:
                old_json = json.load(file)
            except json.JSONDecodeError:
                old_json = []  # empty file case
        if any(item["title"] == data.title for item in old_json):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Note with '{data.title}' title already exists, try saving again with a different title"
            )
        old_json.append(data.model_dump())
        with open(file_path, "w") as file:
            json.dump(old_json, file)
            return data
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Oops! unable to process your request"
        )
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")
    
@app.get("/notes/{title}")
def filter_by_title(title:str):
    try:
        check_filepath() 
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "note.txt")
        with open(file_path, "r") as file:
            try:
                old_json = json.load(file)
            except json.JSONDecodeError:
                old_json = []  # empty file case
        # Find matching notes
        matches = [item for item in old_json if item["title"].lower().strip() == title.lower().strip()]
        if matches:
            return matches
        elif matches == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Note with '{title}' title not found, try searching with a different title")
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")



@app.patch("/notes/{title}")
def update_by_title(title:str, data:Note):
    try:
        check_filepath() 
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "note.txt")
        with open(file_path, "r") as file:
            try:
                old_json = json.load(file)
            except json.JSONDecodeError:
                old_json = []  # empty file case
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
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")

@app.delete("/notes/{title}")
def update_by_title(title:str):
    try:
        check_filepath() 
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "note.txt")
        with open(file_path, "r") as file:
            try:
                old_json = json.load(file)
            except json.JSONDecodeError:
                old_json = []  # empty file case
        # Find the index of the matching note
        for idx, item in enumerate(old_json):
            if item["title"].lower().strip() == title.lower().strip():
                # delete only the fields provided in data
                old_json.pop(idx)
                break
        # Save back to file
        with open(file_path, "w") as f:
            json.dump(old_json, f, indent=4)
            return old_json
        # If no match found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with title '{title}' not found, try updating with a different title"
        )
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")