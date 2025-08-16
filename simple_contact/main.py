from fastapi import FastAPI, HTTPException, status
from typing import Annotated
from pydantic import BaseModel, EmailStr, Field

#calling a fastapi instance
app = FastAPI()

#initializing an empty dataframe
db = {}


#contant class attributes
class Contact(BaseModel):
    name: str = Field(min_length=3)
    phone: str = Field(min_length=11)  #input without the leading zero e.g 9045693432
    email: EmailStr

#endpoints to handle sending new contact details to the server
@app.post("/contacts/", status_code=status.HTTP_201_CREATED)
def add_contact(data:Contact):
    try:
        #condition to trigger if contact name already exist in dictionary
        if data.name in db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"contact with '{data.name}' name already exists, try saving again with a different name"
            )
        #else, create new contact and use name as key
        db[data.name] = data.model_dump()  
        return db
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")
    
#endpoint to handle fetching the contact information for a contact name, more like a search by name 
@app.get("/contacts/", status_code=status.HTTP_200_OK)
def get_contact(name: str):
    #raise an exception if contact name does not exist
    if name not in db:
        raise HTTPException(status_code=404, detail="Contact not found")
    #cdisplay contact information if contact name exist in dictionary
    elif name in db:
        return {name: db[name]}


# endoint to update contact information aside from name
@app.patch("/contacts/{name}", status_code=status.HTTP_200_OK)
def update_contact(data:Contact, name: str):
    try:
        #raise an exception if contact name provided in the path parameter does not exist
        if name not in db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contact with name '{name}' not found"
            )
        # Keep the old name, only update other fields with the information gotten from the body parameters
        existing_contact = db[name]
        updated_contact = {
            "name": existing_contact["name"],  # keep original name
            "phone": data.phone, 
            "email": data.email
        }
        db[name] = updated_contact
        #return the updated contact
        return updated_contact
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")

#endpoint to delete contact from dictionary
@app.delete("/contacts/{name}")
def delete_contact(name: str):
    try:
        #raise and exception if name does not exist in dictionary
        if name not in db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contact with name '{name}' not found"
            )
        #delete the contact information from the dictionary and return the message
        db.pop(name)  # remove from dict
        return {"message": f"Contact '{name}' deleted successfully", "new_db": db}
    #handle try exception
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")