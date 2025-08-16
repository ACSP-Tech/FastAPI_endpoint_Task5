📝 Notes App API

This project is a FastAPI-based Notes Application that allows users to create, update, retrieve, and delete notes.
Notes are stored in a JSON-formatted file (note.txt) to simulate a lightweight file-based database.

🚀 Features

Notes Management

Each note has a title and notes field.

Prevents duplicate note titles.

Supports updating and deleting notes by title.

Endpoints

POST /notes/ → Add a new note

GET /notes/{title} → Retrieve a note by title

PATCH /notes/{title} → Update a note by title

DELETE /notes/{title} → Delete a note by title

File System Support

Notes are stored in note.txt as JSON objects.

Uses os module to create the file if it doesn’t exist.

Ensures persistence across application restarts.

Error Handling

409 Conflict → Duplicate note titles

404 Not Found → Note does not exist

422 Unprocessable Entity → File creation issue

500 Internal Server Error → Unexpected errors

Version Control

Recommended to use Git branches for feature development and testing.

📂 Project Structure
notes-app-api/
│── main.py            # FastAPI app (endpoints for notes)
│── note_utils.py      # Utility function for file handling
│── note.txt           # File-based note storage (auto-created)
│── README.md          # Documentation