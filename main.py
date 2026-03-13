from fastapi import FastAPI, HTTPException, Response
import sqlite3
import csv
import os
from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    bookId: Optional[str] = None
    title: str
    series: Optional[str] = None
    author: Optional[str] = None
    rating: Optional[float] = None
    description: Optional[str] = None
    language: Optional[str] = None
    isbn: Optional[str] = None
    genres: Optional[str] = None
    characters: Optional[str] = None
    bookFormat: Optional[str] = None
    edition: Optional[str] = None
    pages: Optional[int] = None
    publisher: Optional[str] = None
    publishDate: Optional[str] = None
    firstPublishDate: Optional[str] = None
    awards: Optional[str] = None
    numRatings: Optional[int] = None
    ratingsByStars: Optional[str] = None
    likedPercent: Optional[float] = None
    setting: Optional[str] = None
    coverImg: Optional[str] = None
    bbeScore: Optional[float] = None
    bbeVotes: Optional[int] = None
    price: Optional[float] = None


class BookUpdate(BaseModel):
    bookId: Optional[str] = None
    title: Optional[str] = None
    series: Optional[str] = None
    author: Optional[str] = None
    rating: Optional[float] = None
    description: Optional[str] = None
    language: Optional[str] = None
    isbn: Optional[str] = None
    genres: Optional[str] = None
    characters: Optional[str] = None
    bookFormat: Optional[str] = None
    edition: Optional[str] = None
    pages: Optional[int] = None
    publisher: Optional[str] = None
    publishDate: Optional[str] = None
    firstPublishDate: Optional[str] = None
    awards: Optional[str] = None
    numRatings: Optional[int] = None
    ratingsByStars: Optional[str] = None
    likedPercent: Optional[float] = None
    setting: Optional[str] = None
    coverImg: Optional[str] = None
    bbeScore: Optional[float] = None
    bbeVotes: Optional[int] = None
    price: Optional[float] = None

app = FastAPI()

DB_NAME = "books.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def to_int(value):
    if value is None:
        return None
    value = str(value).strip().replace(",", "")
    if value == "":
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def to_float(value):
    if value is None:
        return None
    value = str(value).strip().replace(",", "").replace("£", "").replace("$", "")
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def to_text(value):
    if value is None:
        return None
    value = str(value).strip()
    return value if value != "" else None


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bookId TEXT,
        title TEXT NOT NULL,
        series TEXT,
        author TEXT,
        rating REAL,
        description TEXT,
        language TEXT,
        isbn TEXT,
        genres TEXT,
        characters TEXT,
        bookFormat TEXT,
        edition TEXT,
        pages INTEGER,
        publisher TEXT,
        publishDate TEXT,
        firstPublishDate TEXT,
        awards TEXT,
        numRatings INTEGER,
        ratingsByStars TEXT,
        likedPercent REAL,
        setting TEXT,
        coverImg TEXT,
        bbeScore REAL,
        bbeVotes INTEGER,
        price REAL
    )
    """)

    conn.commit()
    conn.close()


def import_csv():
    if not os.path.exists("books.csv"):
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM books")
    count = cursor.fetchone()[0]

    if count == 0:
        with open("books.csv", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                cursor.execute("""
                INSERT INTO books (
                    bookId, title, series, author, rating, description, language,
                    isbn, genres, characters, bookFormat, edition, pages, publisher,
                    publishDate, firstPublishDate, awards, numRatings, ratingsByStars,
                    likedPercent, setting, coverImg, bbeScore, bbeVotes, price
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    to_text(row.get("bookId")),
                    to_text(row.get("title")),
                    to_text(row.get("series")),
                    to_text(row.get("author")),
                    to_float(row.get("rating")),
                    to_text(row.get("description")),
                    to_text(row.get("language")),
                    to_text(row.get("isbn")),
                    to_text(row.get("genres")),
                    to_text(row.get("characters")),
                    to_text(row.get("bookFormat")),
                    to_text(row.get("edition")),
                    to_int(row.get("pages")),
                    to_text(row.get("publisher")),
                    to_text(row.get("publishDate")),
                    to_text(row.get("firstPublishDate")),
                    to_text(row.get("awards")),
                    to_int(row.get("numRatings")),
                    to_text(row.get("ratingsByStars")),
                    to_float(row.get("likedPercent")),
                    to_text(row.get("setting")),
                    to_text(row.get("coverImg")),
                    to_float(row.get("bbeScore")),
                    to_int(row.get("bbeVotes")),
                    to_float(row.get("price"))
                ))

    conn.commit()
    conn.close()


init_db()
import_csv()


@app.get("/")
def root():
    return {"message": "Book API running"}


@app.get("/books")
def get_books():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books LIMIT 100")
    books = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return {"books": books}


@app.get("/books/{id}")
def get_book(id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books WHERE id = ?", (id,))
    book = cursor.fetchone()

    conn.close()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return dict(book)


@app.post("/books", status_code=201)
def add_book(book: BookCreate):
    conn = get_connection()
    cursor = conn.cursor()

    data = book.model_dump(exclude_none=True)

    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))

    cursor.execute(
        f"INSERT INTO books ({columns}) VALUES ({placeholders})",
        tuple(data.values())
    )

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {"message": "Book added", "id": new_id}


@app.put("/books/{id}")
def update_book(id: int, book: BookUpdate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books WHERE id = ?", (id,))
    existing = cursor.fetchone()

    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Book not found")

    data = book.model_dump(exclude_none=True)

    if not data:
        conn.close()
        raise HTTPException(status_code=400, detail="No fields provided for update")

    updates = ", ".join([f"{key}=?" for key in data.keys()])

    cursor.execute(
        f"UPDATE books SET {updates} WHERE id = ?",
        tuple(data.values()) + (id,)
    )

    conn.commit()
    conn.close()

    return {"message": "Book updated"}

    conn.commit()
    conn.close()

    return {"message": "Book updated"}


@app.delete("/books/{id}", status_code=204)
def delete_book(id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books WHERE id = ?", (id,))
    existing = cursor.fetchone()

    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Book not found")

    cursor.execute("DELETE FROM books WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return Response(status_code=204)

@app.get("/analytics/genre-trends")
def genre_trends():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT genres, COUNT(*) as count
        FROM books
        WHERE genres IS NOT NULL AND genres != ''
        GROUP BY genres
        ORDER BY count DESC
        LIMIT 10
    """)
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return {"genre_trends": results}

@app.get("/analytics/top-rated")
def top_rated():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, author, rating
        FROM books
        WHERE rating IS NOT NULL
        ORDER BY rating DESC
        LIMIT 10
    """)
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return {"top_rated": results}

@app.get("/analytics/rating-distribution")
def rating_distribution():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            CASE
                WHEN rating < 3 THEN 'Below 3'
                WHEN rating >= 3 AND rating < 4 THEN '3 to 3.9'
                WHEN rating >= 4 AND rating < 4.5 THEN '4 to 4.4'
                ELSE '4.5 and above'
            END AS rating_band,
            COUNT(*) AS count
        FROM books
        WHERE rating IS NOT NULL
        GROUP BY rating_band
        ORDER BY count DESC
    """)
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return {"rating_distribution": results}