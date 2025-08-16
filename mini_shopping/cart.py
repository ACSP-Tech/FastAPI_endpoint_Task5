#importing the necessary requirement
from fastapi import HTTPException, status
import pandas as pd
import datetime
import os
import json

#function to handle checking and creating json file with product items
def check_filepath():
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    try:
        import json
        file_path1 = os.path.join(BASE_DIR, "product.json")
        #logic to trigger if product.json does not exist
        if not os.path.exists(file_path1):
            data = {
            "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            "name": [
                "Pasta", "Cheese", "Onions", "Cereal", "Orange Juice", "Ground Beef",
                "Apples", "Tomatoes", "Salmon", "Rice", "Bananas", "Milk", "Eggs", "Bread",
                "Yogurt", "Carrots", "Potatoes", "Chicken Breast"
            ],
            "price": [
                7.46, 1.85, 7.38, 5.5, 8.66, 29.56, 22.13, 2.91, 8.67, 5.58, 10.39, 26.45,
                20.12, 25.92, 3.8, 20.7, 11.28, 10.55
            ]
        }

            # Create DataFrame
            df = pd.DataFrame(data)

            # Convert to JSON
            json_data = json.loads(df.to_json(orient="records"))
            #create and write data to file
            with open(file_path1, "x") as file:
                json.dump(json_data, file)
    except:
       raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Error Creating Json file")
    
#function to handle checking and creating json file with cart item
def CartFilepath():
    #os module handling file path sourcing
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    try:
        import json
        file_path1 = os.path.join(BASE_DIR, "cart.json")
        #logic to trigger if file path does not exist, inessence, create an empty list
        if not os.path.exists(file_path1):
            with open(file_path1, "x") as file:
                json.dump([], file)
    except:
       raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Error Creating Json file")

#function to handle checking and creating json file with checkout history
def append_checkout_history(base_dir, data):
    history_path = os.path.join(base_dir, "checkout_history.json")

    # If history file doesn't exist, create an empty list
    if not os.path.exists(history_path):
        with open(history_path, "w") as f:
            json.dump([], f)
    # Load existing history
    with open(history_path, "r") as f:
        history = json.load(f)

    # Append new checkout entry with timestamp
    history.append({
        "timestamp": datetime.datetime.now().isoformat(),
        "products": data
    })
    # Save back to file
    with open(history_path, "w") as f:
        json.dump(history, f, indent=4)