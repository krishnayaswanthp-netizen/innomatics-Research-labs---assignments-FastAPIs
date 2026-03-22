from fastapi import FastAPI, HTTPException, Query
from models.data import books, users, borrow_records
from schemas.schemas import Book, User, Borrow
from utils.helpers import find_book, find_user, is_book_available

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Library API Running"}

@app.post("/books", status_code=201)
def add_book(book: Book):
    books.append(book.dict())
    return {"message": "Book added"}

@app.get("/books")
def get_books(page: int = 1, limit: int = 5):
    start = (page - 1) * limit
    return books[start:start + limit]

@app.get("/books/{book_id}")
def get_book(book_id: int):
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}")
def update_book(book_id: int, updated: Book):
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.update(updated.dict())
    return {"message": "Book updated"}

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    books.remove(book)
    return {"message": "Book deleted"}

@app.post("/users", status_code=201)
def add_user(user: User):
    users.append(user.dict())
    return {"message": "User added"}

@app.get("/users")
def get_users():
    return users

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = find_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/summary")
def summary():
    return {
        "total_books": len(books),
        "total_users": len(users)
    }

@app.get("/books/count")
def count_books():
    if books:
        return {"total_books": len(books)}
    else:
        raise HTTPException(status_code=404, detail="No books found")

@app.get("/books/search")
def search_books(title: str = Query(None)):
    if title:
        return [b for b in books if title.lower() in b["title"].lower()]
    return books

@app.get("/books/sort")
def sort_books():
    return sorted(books, key=lambda x: x["year"])

@app.get("/books/browse")
def browse_books(
    search: str = Query(None),
    sort: bool = False,
    page: int = 1,
    limit: int = 5
):
    result = books

    if search:
        result = [b for b in result if search.lower() in b["title"].lower()]

    if sort:
        result = sorted(result, key=lambda x: x["year"])

    start = (page - 1) * limit
    return result[start:start + limit]

@app.post("/borrow")
def borrow_book(data: Borrow):
    user = find_user(data.user_id)
    book = find_book(data.book_id)

    if not user or not book:
        raise HTTPException(status_code=404, detail="User or Book not found")

    if not is_book_available(data.book_id):
        raise HTTPException(status_code=400, detail="Book already borrowed")

    borrow_records.append(data.dict())
    return {"message": "Book borrowed"}

@app.post("/return")
def return_book(data: Borrow):
    for record in borrow_records:
        if record["user_id"] == data.user_id and record["book_id"] == data.book_id:
            borrow_records.remove(record)
            return {"message": "Book returned"}

    raise HTTPException(status_code=404, detail="Record not found")

@app.get("/history/{user_id}")
def history(user_id: int):
    return [r for r in borrow_records if r["user_id"] == user_id]