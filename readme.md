

```markdown
# Books API

A FastAPI-based REST API for accessing and querying a books database. This API provides endpoints to search, filter, and retrieve information about books, authors, languages, and subjects.

## Features

- RESTful API endpoints
- Filtering capabilities (by author, language, subject, etc.)
- Pagination support (25 items per page)
- Sorting by download count
- Swagger UI documentation
- MySQL database integration

## Tech Stack

- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **MySQL**: Database
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server implementation

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd books-api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env`:
```env
DATABASE_URL=mysql+mysqlconnector://user:password@localhost/books_db
```

## Database Setup

1. Create MySQL database:
```sql
CREATE DATABASE books_db;
```

2. Import database dump:
```bash
mysql -u root -p books_db < ignite/gutendex.sql
```

## Running the Application

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Books

- `GET /books/`: List all books with pagination
  - Query Parameters:
    - `page`: Page number (default: 1)
    - `limit`: Items per page (default: 25)
    - `title`: Filter by title
    - `author`: Filter by author name
    - `language`: Filter by language code
    - `subject`: Filter by subject
    - `sort_by_downloads`: Sort by download count

- `GET /books/{book_id}`: Get specific book details

### Authors

- `GET /authors/`: List all authors
  - Query Parameters:
    - `page`: Page number
    - `limit`: Items per page
    - `name`: Filter by author name

### Languages

- `GET /languages/`: List all available languages

### Subjects

- `GET /subjects/`: List all subjects
  - Query Parameters:
    - `page`: Page number
    - `limit`: Items per page
    - `name`: Filter by subject name

## Example Usage

```python
import requests

# Get first page of books
response = requests.get("http://localhost:8000/books/")

# Get books by Shakespeare
response = requests.get("http://localhost:8000/books/?author=Shakespeare")

# Get English books about Fiction
response = requests.get("http://localhost:8000/books/?language=en&subject=Fiction")
```

## Project Structure

```
books-api/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI application and endpoints
│   ├── database.py     # Database connection and session
│   ├── models.py       # SQLAlchemy models
│   └── schemas.py      # Pydantic models
├── .env                # Environment variables
└── requirements.txt    # Project dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```
