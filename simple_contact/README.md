📇 Simple Contact API

This project is a FastAPI-based Contact Management System that allows users to create, retrieve, update, and delete contacts.
Contacts are stored in memory using a Python dictionary, making it a lightweight and simple API for learning how to use path and query parameters.

🚀 Features

Contact Model

name → Contact’s name (min 3 characters)

phone → Contact’s phone number (min 11 digits, entered without leading zero, e.g., 9045693432)

email → Contact’s email (validated with Pydantic EmailStr)

Endpoints

POST /contacts/ → Add a new contact

GET /contacts/?name=John → Retrieve a contact by name (query parameter)

PATCH /contacts/{name} → Update a contact (path parameter)

DELETE /contacts/{name} → Delete a contact (path parameter)

In-Memory Storage

Uses a Python dictionary db for storing contacts

No external database required

Error Handling

409 Conflict → Contact with the same name already exists

404 Not Found → Contact not found

500 Internal Server Error → Unexpected issues

📂 Project Structure
simple-contact-api/
│── main.py        # FastAPI app with contact endpoints
│── README.md      # Documentation