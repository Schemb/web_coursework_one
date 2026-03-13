@app.get("/")
def root():
    return {"message": "Book API running"}

@app.get("/books")
def get_books():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT)")
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return {"books": books}

@app.post("/books")
def add_book(title: str, author: str):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO books (title, author) VALUES (?, ?)",
        (title, author)
    )

    conn.commit()
    conn.close()

    return {"message": "Book added"}

@app.put("/books/{book_id}")
def update_book(book_id: int, title: str):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE books SET title=? WHERE id=?",
        (title, book_id)
    )

    conn.commit()
    conn.close()

    return {"message": "Book updated"}

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

    return {"message": "Book deleted"}

