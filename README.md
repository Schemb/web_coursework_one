# Book Metadata and Recommendation API

## Overview
This project is a RESTful web API developed for COMP3011 Web Services and Web Data. It provides CRUD functionality for a book database backed by SQLite and seeded from a CSV dataset. In addition to standard CRUD operations, the API includes analytics endpoints for genre trends, top-rated books, and rating distribution.

## Features
- Create, read, update, and delete book records
- SQLite database integration
- Initial CSV dataset import
- JSON request and response handling
- Analytics endpoints:
  - genre trends
  - top-rated books
  - rating distribution
- Interactive API testing through Swagger UI

## Tech Stack
- Python 3.11
- FastAPI
- SQLite
- Uvicorn
- Pydantic

## Dataset
The API uses a CSV dataset containing book metadata such as title, author, genre, ratings, and publication information. On first run, the dataset is imported into an SQLite database for persistent querying and CRUD operations.

## Project Structure
web_coursework_one/
├── main.py
├── books.csv
├── books.db
├── requirements.txt
├── README.md
└── api_documentation.pdf