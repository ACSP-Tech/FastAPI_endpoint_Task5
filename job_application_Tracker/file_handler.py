#module creating to check and handle json file exception and creation
from fastapi import HTTPException, status

#function to check if json file for saving exist and create if not
def check_filepath():
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    try:
        import json
        file_path1 = os.path.join(BASE_DIR, "applications.json")
        #if filepath is not found, create and write an empty list
        if not os.path.exists(file_path1):
            with open(file_path1, "x") as file:
                json.dump([], file)
    except:
       raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Error Creating Json file")