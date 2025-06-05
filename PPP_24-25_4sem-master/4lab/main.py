from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from . import crud, models, database


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db_session():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors", response_model=models.Author, status_code=status.HTTP_201_CREATED)
def create_author_endpoint(author: models.AuthorCreate, db: Session = Depends(get_db_session)):
    return crud.create_author(db=db, author=author)

@app.get("/authors", response_model=List[models.Author])
def read_authors_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors

@app.get("/authors/{author_id}", response_model=models.Author)
def read_author_endpoint(author_id: int, db: Session = Depends(get_db_session)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return db_author

@app.put("/authors/{author_id}", response_model=models.Author)
def update_author_endpoint(author_id: int, author: models.AuthorCreate, db: Session = Depends(get_db_session)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return crud.update_author(db=db, author_id=author_id, author_update=author)

@app.delete("/authors/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author_endpoint(author_id: int, db: Session = Depends(get_db_session)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    
    crud.delete_author(db=db, author_id=author_id)

# Book Endpoints

@app.post("/books", response_model=models.Book, status_code=status.HTTP_201_CREATED)
def create_book_endpoint(book: models.BookCreate, db: Session = Depends(get_db_session)):
    db_book = crud.create_book(db=db, book=book)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Author with id {book.author_id} not found"
        )
    return db_book

@app.get("/books", response_model=List[models.Book])
def read_books_endpoint(author_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    
    if author_id is not None:
        pass
        
    books = crud.get_books(db, author_id=author_id, skip=skip, limit=limit)
    return books

