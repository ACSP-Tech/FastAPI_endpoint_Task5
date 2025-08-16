#importing the necessary requirement
from fastapi import FastAPI, HTTPException, status
from typing import Annotated
from pydantic import BaseModel, Field
from cart import check_filepath, CartFilepath, append_checkout_history
import os
import json

app = FastAPI()

#product class attributes
class Product(BaseModel):
    id: int
    name: str = Field(min_length=13)
    price: float

#endpoint to view all products available
@app.get("/products/")
def browse_db():
    try:
        #os module handling file path sourcing
        check_filepath()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "product.json")
        #reading and loading json file
        with open(file_path, "r") as file:
            old_json = json.load(file)
    #handling try exception
    except:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Oops! error viewing products, please try again")
    #response: fetching all existing available product
    return old_json

#cart class attributes
class Cart(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    total: float

#endpoint to add item to cart using id and qty query parameters
@app.post("/cart/add")
def add_to_cart(product_id:int, qty:int):
    try:
        #os module handling file path sourcing
        check_filepath()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "product.json")
        #reading and loading json file
        with open(file_path, "r") as file:
            old_json = json.load(file)
        #looping through till a match between parameter id and query id is found
        for item in old_json:
            #condition to execute if match is found 
            if product_id == item["id"]:
                #getting a cart class data, computing for total, extracting name, id, and price
                cart_db = Cart(
                    id =  product_id,
                    name = item["name"],
                    price = item["price"],
                    quantity = qty,
                    total = round(qty * item["price"], 2)
                )
                break
        #if no match is found raise exception
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Product with id {product_id} not found") 
        #excuting after matching, read and load previous cart items
        CartFilepath()
        BASE_DIR2 = os.path.dirname(os.path.abspath(__file__))
        file_path2 = os.path.join(BASE_DIR2, "cart.json")
        with open(file_path2, "r") as file:
            cart_json = json.load(file)
        #append current selection to it
        cart_json.append(cart_db.model_dump())
        #update cart 
        with open(file_path2, "w") as file:
            json.dump(cart_json, file)
        #return the current selection
        return cart_db 
    #handling try exceptions    
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Product with id {product_id} not found")
    except Exception as e:
        # Catches all other unexpected errors and shows them
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")

#endpoint to checkout cart   
@app.get("/cart/checkout")
def checkout_cart():
    try:
        #os module handling and sourcing current cart data
        check_filepath()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "cart.json")
        with open(file_path, "r") as file:
            old_json = json.load(file)
        #exception to raise if no item is found in cart
        if not old_json:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No item in cart to check out")
        # Save checkout history and checkout
        append_checkout_history(BASE_DIR, old_json)
        # Clear the cart 
        with open(file_path, "w") as file:
            json.dump([], file)
        #return the checkout list
        return old_json
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")
        