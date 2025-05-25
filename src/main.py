# main.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pathlib import Path
import csv

app = FastAPI()

# Add CORS middleware to allow GET requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Load data from CSV file
def load_data():
    # Get the current file's directory
    current_file = Path(__file__)
    # Go up one level to reach the project root, then into data folder
    data_path = current_file.parent.parent / 'data' / 'data.csv'
    
    students = []
    with open(data_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            students.append({
                "studentId": int(row["studentId"]),
                "class": row["class"]
            })
    
    return students

# Load data once when the app starts
students_data = load_data()

@app.get("/api")
def get_students(class_filter: Optional[List[str]] = Query(None, alias="class")):
    """
    Get student data, optionally filtered by class.
    
    **Usage Examples:**
    - `/api` → Returns all students
    - `/api?class=1A` → Returns only students in class 1A
    - `/api?class=1A&class=1B` → Returns students in class 1A and 1B
    - `/api?class=8I&class=12Z` → Returns students in class 8I and 12Z
    
    **Response Format:**
    ```json
    {
        "students": [
            {
                "studentId": 1,
                "class": "8I"
            },
            {
                "studentId": 2,
                "class": "2M"
            }
        ]
    }
    ```
    
    Returns students in the same order as they appear in the CSV file.
    """
    if class_filter is None:
        # Return all students
        return {"students": students_data}
    
    # Filter students by the specified classes
    filtered_students = []
    for student in students_data:
        if student["class"] in class_filter:
            filtered_students.append(student)
    
    return {"students": filtered_students}