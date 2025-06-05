from sqlalchemy.orm import Session
from . import models, database


def get_author(db: Session, author_id: int):
    return db.query(models.AuthorDb).filter(models.AuthorDb.id == author_id).first()

def get_author_by_name(db: Session, name: str):
    return db.query(models.AuthorDb).filter(models.AuthorDb.name == name).first()

def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AuthorDb).offset(skip).limit(limit).all()

def create_author(db: Session, author: models.AuthorCreate):
    db_author = models.AuthorDb(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def update_author(db: Session, author_id: int, author_update: models.AuthorCreate):
    db_author = get_author(db, author_id)
    if db_author:
        db_author.name = author_update.name
        db.commit()
        db.refresh(db_author)
    return db_author

def delete_author(db: Session, author_id: int):
    db_author = get_author(db, author_id)
    if db_author:

        db.query(models.BookDb).filter(models.BookDb.author_id == author_id).delete(synchronize_session=False)
        db.delete(db_author)
        db.commit()
        return True
    return False


def get_book(db: Session, book_id: int):
    return db.query(models.BookDb).filter(models.BookDb.id == book_id).first()

def get_books(db: Session, author_id: int = None, skip: int = 0, limit: int = 100):
    query = db.query(models.BookDb)
    if author_id is not None:
        query = query.filter(models.BookDb.author_id == author_id)
    return query.offset(skip).limit(limit).all()

def create_book(db: Session, book: models.BookCreate):
    author = get_author(db, book.author_id)
    if not author:
        return None
        
    db_book = models.BookDb(title=book.title, year=book.year, author_id=book.author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

