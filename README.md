# Donation for Shifa

An open-source donation management platform built with **FastAPI**, **Tortoise ORM**, and **PostgreSQL**. Tracks received donations, records distributions to recipients, and accepts public financial assistance applications — with a transparent, publicly readable API and a secure admin panel.

---

## Features

- **Donation tracking** — admin records every received donation with donor name, transaction number, amount, and date
- **Distribution transparency** — admin logs every distribution to a recipient; visible to the public
- **Public applications** — anyone can submit a financial assistance application; rate-limited to 5 per IP per 24 hours
- **Stats summary** — live aggregated totals (collected vs. distributed) cached in Redis
- **JWT authentication** — Bearer token auth with admin-only role enforcement
- **Django-inspired app layout** — each feature in its own app (`models`, `schemas`, `routes`, `views`, `services`, `tasks`)
- **Per-app migrations** — Aerich migrations per app, stored in `migrations/<app_label>/`
- **Background tasks** — Celery worker + Beat scheduler with Redis broker
- **CORS support** — configurable allowed origins via environment variable

---

## Tech Stack

| Layer         | Technology                        |
|---------------|-----------------------------------|
| Framework     | FastAPI (Python 3.14)             |
| ORM           | Tortoise ORM (async)              |
| Database      | PostgreSQL (SQLite for dev)       |
| Migrations    | Aerich                            |
| Validation    | Pydantic v2                       |
| Auth          | JWT (HS256)                       |
| Cache         | Redis (optional)                  |
| Task queue    | Celery + Redis                    |

---

## Project Structure

```
donation-for-shifa/
├── apps/
│   ├── user/           # Auth — signup, login, profile
│   ├── donation/       # Received donations — admin CRUD + public list
│   ├── distribution/   # Distributions to recipients — admin CRUD + public list
│   ├── application/    # Financial assistance applications — public submit + admin review
│   └── stats/          # Summary stats endpoint (no model)
├── migrations/         # Per-app migration files: migrations/user/, migrations/donation/, ...
├── config/
│   ├── settings.py     # INSTALLED_APPS, DB, Celery, JWT, Redis, CORS
│   ├── db.py           # Tortoise init/close
│   ├── celery.py       # Celery app
│   ├── middleware.py   # JWT auth middleware
│   ├── renderer.py     # Validation/HTTP error responses
│   └── exceptions.py  # ORM exception handlers
├── core/
│   ├── auth.py         # get_current_user, get_admin_user dependencies
│   ├── cache.py        # Optional Redis client
│   └── dependencies.py # Shared FastAPI dependencies
├── utils/
│   ├── jwt.py
│   ├── security.py     # bcrypt password hashing
│   ├── response_wrapper.py
│   ├── pagination.py
│   └── rate_limiter.py # IP-based rate limiter (Redis-backed)
├── main.py
├── manage.py           # CLI: runserver, startapp, makemigrations, migrate, runcelery, ...
├── API.md              # Full API reference with examples
└── env.example
```

---

## Getting Started

### Prerequisites

- Python 3.14
- PostgreSQL
- Redis (optional — for caching and Celery; app degrades gracefully without it)

### Installation

```bash
git clone https://github.com/your-username/donation-for-shifa.git
cd donation-for-shifa

python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

pip install -r requirements.txt   # or: pip install -e .
```

### Environment

```bash
cp env.example .env
```

Edit `.env`:

```env
FASTAPI_ENV=development
DATABASE_URL=postgres://user:password@localhost:5432/donation
REDIS_URL=redis://localhost:6379/1
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
JWT_SECRET_KEY=change-me-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_EXPIRE_MINUTES=1440
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

### Database Setup

```bash
createdb donation

python manage.py makemigrations user
python manage.py makemigrations donation
python manage.py makemigrations distribution
python manage.py makemigrations application
python manage.py migrate
```

### Run the Server

```bash
python manage.py runserver
# API available at http://localhost:8000
# Swagger UI at  http://localhost:8000/docs
# ReDoc at       http://localhost:8000/redoc
```

---

## API Overview

Full documentation with request/response examples is in **[API.md](./API.md)**.

| Method   | Path                                              | Auth   | Description                         |
|----------|---------------------------------------------------|--------|-------------------------------------|
| `POST`   | `/api/v1/user/signup`                             | —      | Register a new user                 |
| `POST`   | `/api/v1/user/token`                              | —      | Obtain JWT token                    |
| `GET`    | `/api/v1/user/me`                                 | JWT    | Current user profile                |
| `GET`    | `/api/v1/donations`                               | —      | Public list of donations            |
| `GET`    | `/api/v1/admin/donations`                         | Admin  | Admin list with search/date filter  |
| `POST`   | `/api/v1/admin/donations`                         | Admin  | Create donation record              |
| `GET`    | `/api/v1/admin/donations/{id}`                    | Admin  | Get donation by ID                  |
| `PUT`    | `/api/v1/admin/donations/{id}`                    | Admin  | Update donation                     |
| `DELETE` | `/api/v1/admin/donations/{id}`                    | Admin  | Delete donation                     |
| `GET`    | `/api/v1/distributions`                           | —      | Public list of distributions        |
| `GET`    | `/api/v1/admin/distributions`                     | Admin  | Admin list with search/date filter  |
| `POST`   | `/api/v1/admin/distributions`                     | Admin  | Create distribution record          |
| `GET`    | `/api/v1/admin/distributions/{id}`                | Admin  | Get distribution by ID              |
| `PUT`    | `/api/v1/admin/distributions/{id}`                | Admin  | Update distribution                 |
| `DELETE` | `/api/v1/admin/distributions/{id}`                | Admin  | Delete distribution                 |
| `POST`   | `/api/v1/applications`                            | —      | Submit assistance application       |
| `GET`    | `/api/v1/admin/applications`                      | Admin  | Admin list with search/status filter|
| `GET`    | `/api/v1/admin/applications/{id}`                 | Admin  | Get application by ID               |
| `PATCH`  | `/api/v1/admin/applications/{id}/status`          | Admin  | Update application status           |
| `GET`    | `/api/v1/stats/summary`                           | —      | Aggregated donation/distribution totals |

---

## Development Commands

```bash
# Start development server
python manage.py runserver

# Scaffold a new app
python manage.py startapp myapp

# Migrations
python manage.py makemigrations <app_label>
python manage.py migrate
python manage.py showmigrations

# Celery worker (development — worker + scheduler in one process)
python manage.py runcelery -B

# Celery worker and Beat separately (production)
python manage.py runbeat          # terminal 1: scheduler
python manage.py runcelery        # terminal 2: worker

# Run a script with DB access
python manage.py runscript pyscript.py
```

---

## Creating an Admin User

After running migrations, create a user via the signup endpoint, then set `is_admin = true` directly in the database:

```bash
psql donation -c "UPDATE users SET is_admin = true WHERE email = 'your@email.com';"
```

---

## Contributing

Contributions are welcome. Please open an issue to discuss your idea before submitting a pull request.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes
4. Open a pull request

---

## License

This project is open source and available under the [MIT License](LICENSE).
