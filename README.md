# BackendAssignment

A FastAPI backend for API key management, per-key rate limiting, and background job processing.

---

## Features

- Generate and manage API keys (UUID-based, SHA256 hashed in DB)
- Per-key rate limiting — 10 requests/minute, returns `429` when exceeded
- Protected `POST /submit-job` endpoint (requires valid API key)
- Background job processing with status tracking (`pending → running → done`)
- `GET /job/{id}` to poll job status and result

---

## Tech Stack

| Layer | Choice |
|---|---|
| Framework | FastAPI |
| Database | SQLite via SQLAlchemy ORM |
| Validation | Pydantic v2 |
| Server | Uvicorn |

---

## Project Structure

```
assignment/
├── app/
│   ├── __init__.py
│   ├── main.py            # app entry, table creation on startup
│   ├── database.py        # SQLAlchemy engine + session
│   ├── models.py          # APIKey and Job ORM models
│   ├── schemas.py         # Pydantic request/response schemas
│   ├── middleware.py      # API key validation (FastAPI dependency)
│   ├── rate_limiter.py    # In-memory sliding window rate limiter
│   ├── routers/
│   │   ├── keys.py        # /keys routes
│   │   └── jobs.py        # /submit-job and /job/{id} routes
│   └── services/
│       ├── key_service.py # key creation, validation, revocation
│       └── job_service.py # job creation + background runner
├── requirements.txt
├── .env.example
├── postman_collection.json
└── README.md
```

---

## Setup & Run

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/BackendAssignment.git
cd BackendAssignment
```

**2. Create a virtual environment (recommended)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the server**
```bash
uvicorn app.main:app --reload
```

Server starts at `http://localhost:8000`

> SQLite database (`app.db`) is created automatically on first run. No migrations needed.

---

## API Documentation

Interactive Swagger UI available at:
```
http://localhost:8000/docs
```

ReDoc available at:
```
http://localhost:8000/redoc
```

---

## API Reference

### Health Check
```
GET /
```
Response:
```json
{ "message": "server is running" }
```

---

### Create API Key
```
POST /keys/
Content-Type: application/json

{ "name": "my-app" }
```
Response:
```json
{
  "id": "uuid",
  "name": "my-app",
  "raw_key": "abc123...",
  "usage_count": 0,
  "created_at": "2024-01-01T00:00:00"
}
```
> **Important:** `raw_key` is only returned once. Save it immediately.

---

### List All Keys
```
GET /keys/
```
Returns all keys (without hashes).

---

### Revoke a Key
```
DELETE /keys/{key_id}
```

---

### Submit a Job *(requires API key)*
```
POST /submit-job
X-API-Key: <your-raw-key>
Content-Type: application/json

{ "payload": "do something useful" }
```
Response:
```json
{
  "id": "job-uuid",
  "status": "pending",
  "result": null,
  "created_at": "2024-01-01T00:00:00"
}
```
Returns `401` if key is missing/invalid.  
Returns `429` if rate limit exceeded (10 req/min per key).

---

### Get Job Status
```
GET /job/{job_id}
```
Response:
```json
{
  "id": "job-uuid",
  "status": "done",
  "result": "processed: do something useful",
  "created_at": "2024-01-01T00:00:00"
}
```
Possible status values: `pending`, `running`, `done`, `failed`

---

## Design Decisions & Assumptions

**SHA256 over bcrypt for key hashing**  
API keys are randomly generated UUIDs — not user-chosen passwords. SHA256 is fast and sufficient. bcrypt's slow hashing is designed for passwords and would add unnecessary latency here.

**In-memory rate limiting**  
A sliding window counter stored in a Python dict. Simple, readable, and works perfectly for a single-server deployment. The trade-off is that it resets on server restart and won't work across multiple instances. Redis would be the right swap for production.

**FastAPI BackgroundTasks over Celery**  
Celery requires a broker (Redis/RabbitMQ), a separate worker process, and significant config overhead. For this scope — simulating async work — BackgroundTasks is the right tool. It runs in the same process and keeps the project self-contained.

**SQLite over Postgres**  
Zero setup, no external service needed. The SQLAlchemy ORM abstracts the DB layer completely — switching to Postgres is a single `DATABASE_URL` env var change.

**Tables created on startup (`create_all`)**  
Fine for development and assignment submission. In production, Alembic migrations would be the correct approach.

---

## Limitations

- Rate limiter state is lost on server restart
- No authentication on `/keys/` endpoints (anyone can create/list/revoke keys)
- Background tasks don't survive server crashes — no persistent job queue
- No pagination on list endpoints
- Single-instance only (rate limiter is in-memory)

---

## What I'd Add Next

- Redis for distributed rate limiting
- Alembic for DB migrations
- Auth middleware on key management routes
- Retry logic for failed jobs
- Pytest + httpx test suite
- Docker + docker-compose setup
