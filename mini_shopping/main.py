from fastapi import FastAPI, HTTPException, status
from typing import Annotated
from pydantic import BaseModel, Field
from cart import check_filepath, CartFilepath, append_checkout_history
import os
import json

app = FastAPI()

#post request for adding cart
class Product(BaseModel):
    id: int
    name: str = Field(min_length=13)
    price: float

@app.get("/products/")
def browse_db():
    try:
        check_filepath()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "product.json")
        with open(file_path, "r") as file:
            old_json = json.load(file)
    except:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Oops! error viewing products, please try again")
    return old_json

class Cart(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    total: float

@app.post("/cart/add")
def add_to_cart(product_id:int, qty:int):
    try:
        check_filepath()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "product.json")
        with open(file_path, "r") as file:
            old_json = json.load(file)
        for item in old_json:
            if product_id == item["id"]:
                cart_db = Cart(
                    id =  product_id,
                    name = item["name"],
                    price = item["price"],
                    quantity = qty,
                    total = round(qty * item["price"], 2)
                )
                break
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Product with id {product_id} not found") 
        CartFilepath()
        BASE_DIR2 = os.path.dirname(os.path.abspath(__file__))
        file_path2 = os.path.join(BASE_DIR2, "cart.json")
        with open(file_path2, "r") as file:
            cart_json = json.load(file)
        cart_json.append(cart_db.model_dump())
        with open(file_path2, "w") as file:
            json.dump(cart_json, file)
        return cart_db     
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Product with id {product_id} not found")
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")

   
@app.get("/cart/checkout")
def checkout_cart():
    try:
        check_filepath()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "cart.json")
        with open(file_path, "r") as file:
            old_json = json.load(file)
        if not old_json:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No item in cart to check out")
        # Save checkout history
        append_checkout_history(BASE_DIR, old_json)
        # Clear the product.json file
        with open(file_path, "w") as file:
            json.dump([], file)
        return old_json
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")
        