from fastapi import FastAPI, HTTPException
import sqlite3
import csv
import os

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
def add_book(book: dict):
    conn = get_connection()
    cursor = conn.cursor()

    allowed_fields = [
        "bookId","title","series","author","rating","description","language",
        "isbn","genres","characters","bookFormat","edition","pages","publisher",
        "publishDate","firstPublishDate","awards","numRatings","ratingsByStars",
        "likedPercent","setting","coverImg","bbeScore","bbeVotes","price"
    ]

    filtered_book = {k: v for k, v in book.items() if k in allowed_fields}

    columns = ", ".join(filtered_book.keys())
    placeholders = ", ".join(["?"] * len(filtered_book))

    cursor.execute(
        f"INSERT INTO books ({columns}) VALUES ({placeholders})",
        tuple(filtered_book.values())
    )

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {"message": "Book added", "id": new_id}


@app.put("/books/{id}")
def update_book(id: int, book: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books WHERE id = ?", (id,))
    existing = cursor.fetchone()

    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Book not found")

    updates = ", ".join([f"{key}=?" for key in book.keys()])

    cursor.execute(
        f"UPDATE books SET {updates} WHERE id = ?",
        tuple(book.values()) + (id,)
    )

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