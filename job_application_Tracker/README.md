**Job Application Tracker API**

This project is a FastAPI-based Job Application Tracker that helps you manage and search your job applications.
It stores applications in a JSON file (applications.json) and provides REST API endpoints for adding, viewing, and filtering job applications.

**Features**

**JobApplication Model:**
Each application contains:

name → Applicant’s name

company → Company applied to

position → Job role

status → Application status (e.g., pending, accepted, in progress)

Endpoints:

POST /applications/ → Add a new job application

GET /applications/ → View all job applications

GET /applications/search?status=pending → Search/filter applications by status

File Handling

Data is saved in applications.json

If the file does not exist, it will be created automatically

Uses a helper function in file_handler.py

Error Handling

Invalid requests return 422 Unprocessable Entity

Unexpected issues return 500 Internal Server Error

Missing search results return 404 Not Found

📂 Project Structure
job-tracker-api/
│── file_handler.py       # Handles JSON file creation/checks
│── main.py               # FastAPI application
│── applications.json     # Data store (auto-created)
│── README.md             # Project documentation