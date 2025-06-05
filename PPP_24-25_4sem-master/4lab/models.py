import datetime
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, field_validator, ConfigDict

from .database import Base

# SQLAlchemy models
class AuthorDb(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    books = relationship("BookDb", back_populates="author")

class BookDb(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    year = Column(Integer)
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("AuthorDb", back_populates="books")

# Pydantic models (schemas)

# Author schemas
class AuthorBase(BaseModel):
    name: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Book schemas
class BookBase(BaseModel):
    title: str
    year: int
    author_id: int

    @field_validator('year')
    def validate_year(cls, value):
        current_year = datetime.date.today().year
        if value > current_year:
            raise ValueError("Год издания не может быть в будущем")
        return value

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    # author: Author # Optional: if you want to nest author details in book response

    model_config = ConfigDict(from_attributes=True)

class BookWithAuthor(Book): # For GET /books to show author details if needed
    # This matches the example [{id, название, год, author_id}, ...]
    # If we need full author object, we can change this.
    pass 