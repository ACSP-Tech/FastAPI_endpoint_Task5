from fastapi import HTTPException, status

def check_filepath():
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    try:
        file_path1 = os.path.join(BASE_DIR, "note.txt")
        if not os.path.exists(file_path1):
            with open(file_path1, "x") as file:
                file.write("")
    except:
       raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Error Creating Json file")