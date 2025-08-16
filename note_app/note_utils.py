#import necessary requirement
from fastapi import HTTPException, status

#function to source for filepath and create if it does not exist
def check_filepath():
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    try:
        file_path1 = os.path.join(BASE_DIR, "note.txt")
        #tiggers if file path does not exist
        if not os.path.exists(file_path1):
            with open(file_path1, "x") as file:
                file.write("")
    #handling try exceptions
    except:
       raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Error Creating Json file")