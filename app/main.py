import os
from fastapi import FastAPI, Query, HTTPException, Depends, Path
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session
import logging
from .database import get_db
from .models import Book, Author, Language, Subject
from .schemas import BookResponse, AuthorResponse, LanguageResponse, SubjectResponse

# Get port from environment variable
port = int(os.environ.get("PORT", 8000))

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Books API",
    description="API to query and access books from database",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to the Books API",
        "version": "1.0.0",
        "endpoints": [
            "/books",
            "/books/{book_id}",
            "/authors",
            "/languages",
            "/subjects"
        ]
    }

@app.get("/books/")
async def get_books(
    db: Session = Depends(get_db),
    page: int = Query(1, gt=0, description="Page number"),
    limit: int = Query(25, le=100, description="Items per page"),
    title: Optional[str] = None,
    author: Optional[str] = None,
    language: Optional[str] = None,
    subject: Optional[str] = None,
    sort_by_downloads: bool = False
):
    """
    Get a list of books with optional filters and pagination
    """
    try:
        skip = (page - 1) * limit
        query = select(Book)

        # Apply filters
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
        if author:
            query = query.join(Book.authors).filter(Author.name.ilike(f"%{author}%"))
        if language:
            query = query.join(Book.languages).filter(Language.code == language)
        if subject:
            query = query.join(Book.subjects).filter(Subject.name.ilike(f"%{subject}%"))
        
        # Apply sorting
        if sort_by_downloads:
            query = query.order_by(Book.download_count.desc())

        # Get total count
        total = db.scalar(select(func.count()).select_from(query.subquery()))
        
        # Get paginated results
        books = db.scalars(query.offset(skip).limit(limit)).all()
        
        return {
            "total": total,
            "page": page,
            "per_page": limit,
            "books": [
                {
                    "id": book.id,
                    "title": book.title,
                    "download_count": book.download_count,
                    "authors": [{"name": author.name, "birth_year": author.birth_year} for author in book.authors],
                    "languages": [lang.code for lang in book.languages],
                    "subjects": [subject.name for subject in book.subjects]
                }
                for book in books
            ]
        }
    except Exception as e:
        logger.error(f"Error in get_books: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/books/{book_id}")
async def get_book(
    book_id: int = Path(..., title="The ID of the book to get"),
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific book by ID
    """
    try:
        query = select(Book).filter(Book.id == book_id)
        book = db.scalar(query)
        
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
            
        return {
            "id": book.id,
            "title": book.title,
            "download_count": book.download_count,
            "authors": [
                {
                    "name": author.name,
                    "birth_year": author.birth_year,
                    "death_year": author.death_year
                }
                for author in book.authors
            ],
            "languages": [lang.code for lang in book.languages],
            "subjects": [subject.name for subject in book.subjects]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_book: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/authors/")
async def get_authors(
    db: Session = Depends(get_db),
    page: int = Query(1, gt=0, description="Page number"),
    limit: int = Query(25, le=100, description="Items per page"),
    name: Optional[str] = None
):
    """
    Get a list of authors with optional name filter
    """
    try:
        skip = (page - 1) * limit
        query = select(Author)
        
        if name:
            query = query.filter(Author.name.ilike(f"%{name}%"))
        
        total = db.scalar(select(func.count()).select_from(query.subquery()))
        authors = db.scalars(query.offset(skip).limit(limit)).all()
        
        return {
            "total": total,
            "page": page,
            "per_page": limit,
            "authors": [
                {
                    "id": author.id,
                    "name": author.name,
                    "birth_year": author.birth_year,
                    "death_year": author.death_year,
                    "book_count": len(author.books)
                }
                for author in authors
            ]
        }
    except Exception as e:
        logger.error(f"Error in get_authors: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/languages/")
async def get_languages(db: Session = Depends(get_db)):
    """
    Get a list of all available languages
    """
    try:
        query = select(Language)
        languages = db.scalars(query).all()
        
        return {
            "total": len(languages),
            "languages": [
                {
                    "code": lang.code,
                    "book_count": len(lang.books)
                }
                for lang in languages
            ]
        }
    except Exception as e:
        logger.error(f"Error in get_languages: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/subjects/")
async def get_subjects(
    db: Session = Depends(get_db),
    page: int = Query(1, gt=0, description="Page number"),
    limit: int = Query(25, le=100, description="Items per page"),
    name: Optional[str] = None
):
    """
    Get a list of subjects/topics with optional name filter
    """
    try:
        skip = (page - 1) * limit
        query = select(Subject)
        
        if name:
            query = query.filter(Subject.name.ilike(f"%{name}%"))
        
        total = db.scalar(select(func.count()).select_from(query.subquery()))
        subjects = db.scalars(query.offset(skip).limit(limit)).all()
        
        return {
            "total": total,
            "page": page,
            "per_page": limit,
            "subjects": [
                {
                    "id": subject.id,
                    "name": subject.name,
                    "book_count": len(subject.books)
                }
                for subject in subjects
            ]
        }
    except Exception as e:
        logger.error(f"Error in get_subjects: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Error Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return {
        "error": "Internal server error",
        "status_code": 500
    }