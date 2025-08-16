from fastapi import FastAPI, HTTPException, status
from typing import Annotated
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

db = {}


#post request for adding contact
class Contact(BaseModel):
    name: str = Field(min_length=3)
    phone: str = Field(min_length=11)  #input without the leading zero e.g 9045693432
    email: EmailStr

@app.post("/contacts/", status_code=status.HTTP_201_CREATED)
def add_contact(data:Contact):
    try:
        if data.name in db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"contact with '{data.name}' name already exists, try saving again with a different name"
            )
        db[data.name] = data.model_dump()  
        return db
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")
    

@app.get("/contacts/", status_code=status.HTTP_200_OK)
def get_contact(name: str):
    if name not in db:
        raise HTTPException(status_code=404, detail="Contact not found")
    elif name in db:
        return {name: db[name]}


# 3. POST /contacts/{name} -> Update contact using path parameter
@app.patch("/contacts/{name}", status_code=status.HTTP_200_OK)
def update_contact(data:Contact, name: str):
    try:
        if name not in db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contact with name '{name}' not found"
            )
        # Keep the old name, only update other fields
        existing_contact = db[name]
        updated_contact = {
            "name": existing_contact["name"],  # keep original name
            "phone": data.phone or existing_contact.get("phone"),
            "email": data.email or existing_contact.get("email")
        }
        db[name] = updated_contact
        return updated_contact
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")

@app.delete("/contacts/{name}")
def delete_contact(name: str):
    try:
        if name not in db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contact with name '{name}' not found"
            )
        deleted_contact = db.pop(name)  # remove from dict
        return {"message": f"Contact '{name}' deleted successfully", "deleted": deleted_contact}
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")