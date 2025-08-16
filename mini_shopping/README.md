🛒 Mini Shopping API with Cart

This project is a FastAPI-based Shopping API that allows users to browse products, add them to a cart, and checkout.
It uses JSON files for storage and maintains a checkout history for tracking purchases.

🚀 Features

Product Catalog

Each product has an id, name, and price

Preloaded with 18 grocery items

Cart Management

Add products to the cart with a specific quantity

Automatically calculates the total price per item

Cart data is stored in cart.json

Checkout System

Fetch all items in the cart

Save checkout history to checkout_history.json with a timestamp

Clear cart after checkout

File Handling (cart.py)

check_filepath() → Initializes product list (product.json)

CartFilepath() → Initializes cart file (cart.json)

append_checkout_history() → Saves checkout history

Error Handling

Invalid product IDs return 404 Not Found

Empty cart checkout returns 404 Not Found

Unexpected errors return 500 Internal Server Error

📂 Project Structure
mini-shopping-api/
│── main.py                  # FastAPI app (endpoints)
│── cart.py                  # Handles product/cart file operations
│── product.json             # Product database (auto-created)
│── cart.json                # Cart storage (auto-created)
│── checkout_history.json    # Checkout logs with timestamps (auto-created)
│── README.md                # Project documentation