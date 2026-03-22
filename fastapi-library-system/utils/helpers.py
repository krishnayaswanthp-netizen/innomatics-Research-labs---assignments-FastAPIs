from models.data import books, users, borrow_records

def find_book(book_id):
    for book in books:
        if book["id"] == book_id:
            return book
    return None

def find_user(user_id):
    for user in users:
        if user["id"] == user_id:
            return user
    return None

def is_book_available(book_id):
    for record in borrow_records:
        if record["book_id"] == book_id:
            return False
    return True
