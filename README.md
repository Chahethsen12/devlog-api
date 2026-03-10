# DevLog API 🛠️

A production-grade REST API for logging daily developer activity. Track what you built, how long you coded, and how you felt — with JWT authentication, pagination, filtering, unit tests, and CI/CD.

![CI](https://github.com/Chahethsen12/devlog-api/actions/workflows/ci.yml/badge.svg)

## Features

- **JWT Authentication** — Secure register and login
- **Full CRUD** — Create, read, update, delete log entries
- **Pagination** — `?page=1&limit=10`
- **Filtering** — `?language=python&mood=focused`
- **14 Unit Tests** — All passing
- **CI/CD Pipeline** — GitHub Actions runs tests on every push
- **Docker Ready** — Run anywhere with one command

## Tech Stack

- **FastAPI** — Python web framework
- **PostgreSQL** — Database (Supabase)
- **SQLAlchemy** — ORM
- **JWT** — Authentication
- **pytest** — Unit testing
- **GitHub Actions** — CI/CD
- **Docker** — Containerization

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL database (or Supabase)

### Installation
```bash
git clone https://github.com/Chahethsen12/devlog-api.git
cd devlog-api
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
pip install bcrypt==4.0.1
```

### Environment Variables

Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://postgres:yourpassword@db.xxxx.supabase.co:5432/postgres?sslmode=require
SECRET_KEY=your-secret-key
```

### Run
```bash
uvicorn app.main:app --reload
```

API is live at `http://localhost:8000`
Swagger docs at `http://localhost:8000/docs`

### Run with Docker
```bash
docker build -t devlog-api .
docker run -p 8000:8000 --env-file .env devlog-api
```

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create account |
| POST | `/auth/login` | Login and get JWT token |

### Logs
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/logs/` | Create a log entry |
| GET | `/logs/` | Get all logs (paginated) |
| GET | `/logs/{id}` | Get a single log |
| PATCH | `/logs/{id}` | Update a log |
| DELETE | `/logs/{id}` | Delete a log |

### Query Parameters
| Parameter | Example | Description |
|-----------|---------|-------------|
| `page` | `?page=2` | Page number |
| `limit` | `?limit=5` | Results per page |
| `language` | `?language=python` | Filter by language |
| `mood` | `?mood=focused` | Filter by mood |

## Example Usage

**Register:**
```json
POST /auth/register
{
  "email": "dev@example.com",
  "password": "Password123"
}
```

**Create a log:**
```json
POST /logs/
Authorization: Bearer <token>

{
  "title": "Built JWT auth system",
  "language": "python",
  "duration_minutes": 90,
  "mood": "focused",
  "tags": "auth, jwt, fastapi"
}
```

**Get logs with filters:**
```
GET /logs/?language=python&mood=focused&page=1&limit=10
Authorization: Bearer <token>
```

## Running Tests
```bash
pytest app/tests/ -v
```

Expected output: **14 passed**

## Project Structure
```
devlog-api/
├── app/
│   ├── main.py           # FastAPI app entry point
│   ├── database.py       # Database connection
│   ├── models/
│   │   ├── user.py       # User model
│   │   └── log.py        # Log model
│   ├── routes/
│   │   ├── auth.py       # Auth endpoints
│   │   └── logs.py       # Log endpoints
│   ├── services/
│   │   └── auth_service.py  # JWT + password hashing
│   └── tests/
│       ├── test_auth.py  # Auth tests
│       └── test_logs.py  # Log tests
├── .github/
│   └── workflows/
│       └── ci.yml        # GitHub Actions CI
├── Dockerfile
├── requirements.txt
└── README.md
```

## License

MIT

## 👨‍💻 Author

**Chaheth Senevirathne**
- GitHub: [@chahethsen12](https://github.com/chahethsen12)
- LinkedIn: [chaheth-senevirathne](https://linkedin.com/in/chaheth-senevirathne)