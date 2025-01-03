from pydantic import BaseModel
from typing import List, Optional

class AuthorResponse(BaseModel):
    id: int
    name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    book_count: Optional[int] = None

    class Config:
        from_attributes = True

class LanguageResponse(BaseModel):
    code: str
    book_count: Optional[int] = None

    class Config:
        from_attributes = True

class SubjectResponse(BaseModel):
    id: int
    name: str
    book_count: Optional[int] = None

    class Config:
        from_attributes = True

class BookResponse(BaseModel):
    id: int
    title: str
    download_count: Optional[int] = None
    authors: List[AuthorResponse]
    languages: List[str]
    subjects: List[str]

    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    total: int
    page: int
    per_page: int
    items: List[BookResponse]

    class Config:
        from_attributes = True