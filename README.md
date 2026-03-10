# DevLog API

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-green?logo=githubactions)
![Tests](https://img.shields.io/badge/Tests-14%2F14_passing-brightgreen)
![Deploy](https://img.shields.io/badge/Deploy-Railway-purple?logo=railway)

A production-ready REST API for logging daily developer activity. Built with FastAPI, PostgreSQL, JWT authentication, and a full CI/CD pipeline via GitHub Actions.

**Live API:** `https://devlog-api-production.up.railway.app/docs`

---

## Features

- JWT authentication (register, login)
- Create, read, and delete dev logs
- Filter logs by language and mood
- Pagination support
- 14 automated tests (pytest)
- CI/CD with GitHub Actions
- Dockerized for deployment

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Auth | JWT + bcrypt |
| Testing | pytest |
| CI/CD | GitHub Actions |
| Deployment | Railway |

---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and get JWT token |

### Logs
| Method | Endpoint | Description |
|---|---|---|
| POST | `/logs/` | Create a new dev log |
| GET | `/logs/` | Get all logs (paginated) |
| GET | `/logs/{id}` | Get a specific log |
| DELETE | `/logs/{id}` | Delete a log |

### Filtering & Pagination
```
GET /logs/?language=python&mood=focused&page=1&limit=10
```

---

## Log Schema

```json
{
  "title": "Built auth system",
  "description": "Implemented JWT login and register endpoints",
  "language": "python",
  "duration_minutes": 120,
  "mood": "focused",
  "tags": ["fastapi", "jwt", "auth"]
}
```

---

## Run Locally

**Prerequisites:** Python 3.11+, PostgreSQL

```bash
# Clone the repo
git clone https://github.com/Chahethsen12/devlog-api.git
cd devlog-api

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your DATABASE_URL and SECRET_KEY

# Run the server
uvicorn app.main:app --reload
```

API docs available at: `http://localhost:8000/docs`

---

## Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/devlog
SECRET_KEY=your-secret-key-here
```

---

## Running Tests

```bash
pytest app/tests/ -v
```

Tests use SQLite in-memory database — no PostgreSQL required for CI.

---

## CI/CD

GitHub Actions automatically runs all 14 tests on every push to `main`.

```
.github/workflows/ci.yml
```

---

## Project Structure

```
devlog-api/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   │   ├── user.py
│   │   └── log.py
│   ├── routes/
│   │   ├── auth.py
│   │   └── logs.py
│   ├── services/
│   │   └── auth_service.py
│   └── tests/
│       ├── test_auth.py
│       └── test_logs.py
├── .github/workflows/ci.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

---

## License

MIT

---

## 👨‍💻 Author

**Chaheth Senevirathne**
- GitHub: [@chahethsen12](https://github.com/chahethsen12)
- LinkedIn: [chaheth-senevirathne](https://linkedin.com/in/chaheth-senevirathne)