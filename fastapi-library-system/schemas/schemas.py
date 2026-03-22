from pydantic import BaseModel, Field

class Book(BaseModel):
    id: int
    title: str = Field(..., min_length=1)
    author: str
    year: int = Field(..., gt=0)

class User(BaseModel):
    id: int
    name: str = Field(..., min_length=1)

class Borrow(BaseModel):
    user_id: int
    book_id: int