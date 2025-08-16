#importing the necessary requirement
from fastapi import HTTPException, status

#function to handling filepath exceptions and creation if necessary
def check_filepath():
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    try:
        import json
        file_path1 = os.path.join(BASE_DIR, "student_result.json")
        if not os.path.exists(file_path1):
            with open(file_path1, "x") as file:
                json.dump([], file)
    except:
       raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Error Creating Json file")

#function and logic to compute grade (A to F)   
def compute_grade(grade_score: float) -> str:
    if grade_score >= 90:
        return "A"
    elif grade_score >= 80:
        return "B"
    elif grade_score >= 70:
        return "C"
    elif grade_score >= 60:
        return "D"
    elif grade_score >= 50:
        return "E"
    else:
        return "F"