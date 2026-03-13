# Book Metadata and Recommendation API

## Overview
This project is a RESTful web API developed for the **COMP3011 Web Services and Web Data** coursework. The API provides CRUD (Create, Read, Update, Delete) functionality for a book database backed by **SQLite** and seeded from a **CSV dataset** containing book metadata.

In addition to basic CRUD operations, the API also includes analytics endpoints that provide insights into the dataset, such as:

- genre trends
- top-rated books
- rating distribution

The API is implemented using **FastAPI**, which provides automatic request validation, JSON responses, and interactive documentation via Swagger UI.

---

## Features
- Create, read, update, and delete book records
- SQLite database integration
- Initial CSV dataset import on first run
- JSON request and response handling
- Analytics endpoints for:
  - genre trends
  - top-rated books
  - rating distribution
- Interactive API testing through Swagger UI

---

## Tech Stack
- Python 3.11
- FastAPI
- SQLite
- Uvicorn
- Pydantic

FastAPI was chosen because it provides lightweight API development, automatic validation, and built-in interactive documentation.

SQLite was chosen because it is simple to set up, lightweight, and appropriate for a coursework-sized project.

---

## Dataset
The API uses a CSV dataset containing book metadata, including:

- title
- author
- genres
- ratings
- publication details
- pricing information

When the application starts for the first time, the dataset is automatically imported into an SQLite database. This allows the API to perform CRUD operations and analytics queries against a persistent database rather than directly reading from the CSV file.

The database uses an auto-incrementing `id` field as the primary key, while the original dataset identifier (`bookId`) is stored as a normal attribute.

---

## Project Structure

web_coursework_one/
├── main.py
├── books.csv
├── books.db
├── requirements.txt
├── README.md
└── api_documentation.pdf

- **main.py** – FastAPI application containing all endpoints and database logic  
- **books.csv** – Source dataset used to populate the database  
- **books.db** – SQLite database created automatically on first run  
- **requirements.txt** – Python dependencies  
- **README.md** – Project documentation  
- **api_documentation.pdf** – Detailed API documentation  

---

## Installation and Setup

### 1. Clone the repository

git clone [<your-repository-url>](https://github.com/Schemb/web_coursework_one.git)
cd web_coursework_one

### 2. Create a virtual environment

python3 -m venv venv

### 3. Activate the virtual environment

Mac / Linux:

source venv/bin/activate

Windows:

venv\Scripts\activate

### 4. Install dependencies

pip install -r requirements.txt

### 5. Run the API

uvicorn main:app --reload

---

## Accessing the API

Once the server is running, open one of the following:

Swagger UI (interactive documentation):

http://127.0.0.1:8000/docs

ReDoc documentation:

http://127.0.0.1:8000/redoc

---

## API Endpoints

| Method | Endpoint                         | Description                              |
|--------|----------------------------------|------------------------------------------|
| GET    | `/`                              | Root route to confirm the API is running |
| GET    | `/books`                         | Retrieve a list of books                 |
| GET    | `/books/{id}`                    | Retrieve a single book by database ID    |
| POST   | `/books`                         | Create a new book                        |
| PUT    | `/books/{id}`                    | Update an existing book                  |
| DELETE | `/books/{id}`                    | Delete a book                            |
| GET    | `/analytics/genre-trends`        | Return the most common genres            |
| GET    | `/analytics/top-rated`           | Return the top-rated books               |
| GET    | `/analytics/rating-distribution` | Return rating distribution bands         |

---

## Example Request

Create a new book:

{
  "title": "Example Book",
  "author": "Jane Doe",
  "rating": 4.5,
  "language": "English"
}

---

## Example Response

{
  "message": "Book added",
  "id": 101
}

---

## API Documentation

Full API documentation is included in the repository:

api_documentation.pdf

Interactive documentation is also available via Swagger UI when the server is running.

---

## Limitations

- No authentication is currently implemented
- Some dataset fields are stored as text rather than normalized relational tables
- Analytics endpoints use basic SQL aggregation
- Dataset quality may contain inconsistent formatting due to the original CSV source

---

## Future Improvements

Possible future enhancements include:

- Adding authentication for write endpoints
- Implementing filtering and search functionality
- Normalizing database tables (e.g., authors, genres)
- Implementing more advanced recommendation algorithms
- Deploying the API to a public hosting platform

---

## References

- FastAPI Documentation
- SQLite Documentation
- Source book metadata dataset

---

## Note on Generative AI

Generative AI tools were used during development to assist with debugging, design planning, and code refinement. Full disclosure of AI usage is provided in the accompanying technical report, including examples of prompts and generated responses in the appendix.