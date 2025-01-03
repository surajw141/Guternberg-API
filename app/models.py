from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Association tables
book_authors = Table(
    'books_book_authors',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books_book.id')),
    Column('author_id', Integer, ForeignKey('books_author.id'))
)

book_languages = Table(
    'books_book_languages',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books_book.id')),
    Column('language_id', Integer, ForeignKey('books_language.id'))
)

book_subjects = Table(
    'books_book_subjects',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books_book.id')),
    Column('subject_id', Integer, ForeignKey('books_subject.id'))
)

# Add to your existing models.py
class Format(Base):
    __tablename__ = "books_format"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books_book.id'))
    mime_type = Column(String)
    url = Column(String)

    book = relationship("Book", back_populates="formats")

# Update Book class to include formats


class Book(Base):
    __tablename__ = "books_book"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    download_count = Column(Integer)
    
    authors = relationship("Author", secondary=book_authors, back_populates="books")
    languages = relationship("Language", secondary=book_languages, back_populates="books")
    subjects = relationship("Subject", secondary=book_subjects, back_populates="books")
    formats = relationship("Format", back_populates="book")

class Author(Base):
    __tablename__ = "books_author"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birth_year = Column(Integer)
    death_year = Column(Integer)
    
    books = relationship("Book", secondary=book_authors, back_populates="authors")

class Language(Base):
    __tablename__ = "books_language"

    id = Column(Integer, primary_key=True)
    code = Column(String)
    
    books = relationship("Book", secondary=book_languages, back_populates="languages")

class Subject(Base):
    __tablename__ = "books_subject"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    books = relationship("Book", secondary=book_subjects, back_populates="subjects")

