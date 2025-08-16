📘 Student Result Management API

A simple FastAPI-based API for managing student results, computing grades, and storing data in a JSON file. This project is designed to practice REST API concepts, error handling, and file-based persistence.

🚀 Features

Add new student results with computed grades (A–F).

Fetch student results by name (case-insensitive search).

View all student records in the database.

JSON-based persistence (student_result.json file).

Robust error handling using FastAPI’s HTTPException.

🛠️ Tech Stack

FastAPI – API framework

Pydantic – Data validation

JSON – File storage

Uvicorn – ASGI server

📂 Project Structure
.
├── students_utils.py     # Utility functions (file handling + grade computation)
├── main.py               # Main FastAPI app
├── student_result.json   # Auto-created JSON database for student records
└── README.md             # Project documentation