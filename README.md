# FastAPI Boilerplate

A Django-inspired FastAPI structure for rapid API development on **Python 3.14**, with Tortoise ORM, Pydantic v2, Celery, and JWT auth.

## Requirements

- **Python 3.14** (see `.python-version`)
- Redis (for Celery broker/backend and optional auth cache)
- SQLite (default dev DB), or PostgreSQL/MySQL via `DATABASE_URL`

## Features

- **Django-like app layout**: Discrete apps (`apps/user`, `apps/posts`, …) with `models.py`, `schemas.py`, `routes.py`, `views.py`, `services.py`, `tasks.py`
- **Django-like migrations**: Per-app migrations with Aerich (`makemigrations <app>`, `migrate`)
- **Tortoise ORM**: Async ORM with connection pooling and Pydantic v2 serialization
- **Pydantic v2**: Request/response schemas with `model_validate` and `from_attributes`
- **Celery**: Background tasks with Redis broker; CLI `python manage.py runcelery`
- **JWT auth**: Bearer tokens, `request.state.user`, optional Redis user cache
- **CLI**: `python manage.py startapp`, `runserver`, `runcelery`, `runbeat`, `runscript`, `makemigrations`, `migrate`
- **OpenAPI**: Tags and response models per app for Swagger/ReDoc

## Project structure

```
fastapi-boilerplate/
├── apps/
│   ├── user/           # Auth app (signup, token, me)
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── routes.py
│   │   ├── views.py
│   │   ├── services.py
│   │   └── tasks.py
│   └── ...
├── migrations/         # Per-app migration files (Aerich): migrations/user/, migrations/posts/, ...
├── config/
│   ├── settings.py     # INSTALLED_APPS, DB, Celery, JWT, Redis
│   ├── db.py
│   ├── celery.py
│   ├── middleware.py  # JWT auth + process-time
│   ├── renderer.py    # Validation/HTTP error responses
│   └── exceptions.py  # ORM (DoesNotExist, IntegrityError) handlers
├── core/
│   ├── auth.py        # get_current_user, get_current_user_optional
│   ├── serializers.py # Base Pydantic/Tortoise serialization patterns
│   └── dependencies.py
├── utils/             # jwt, security, response_wrapper, pagination, etc.
├── main.py
└── manage.py
```

## Create a new app

```bash
python manage.py startapp myapp
```

Then add `apps.myapp` to `INSTALLED_APPS` in `config/settings.py`.

## Register apps

In `config/settings.py`:

```python
INSTALLED_APPS = [
    "apps.user",
    # "apps.posts",
]
```

## Run the API

```bash
python manage.py runserver
```

Options: `--host 0.0.0.0 --port 8000`

## Run a script (with DB)

```bash
python manage.py runscript pyscript.py
```

## Celery worker and beat

### Production: run Beat and worker separately (recommended)

Run **one** Celery Beat process (scheduler) and **one or more** worker processes. Beat only enqueues periodic tasks; workers execute them. This keeps scheduling reliable and lets you scale workers independently.

**Terminal 1 – Beat (scheduler):**

```bash
python manage.py runbeat
```

**Terminal 2 – Worker(s):**

```bash
python manage.py runcelery
```

Optional Beat options: `-s/--schedule` (schedule DB path), `-l/--loglevel`, `-f/--logfile`, `--pidfile`, `--max-interval`. Example with a custom schedule file and pidfile (e.g. for a process manager):

```bash
python manage.py runbeat -s /var/run/celery/celerybeat-schedule --pidfile /var/run/celery/beat.pid
```

### Development / simple setup: worker with embedded Beat

You can run the scheduler in the **same process** as the worker using the `-B` flag. This is convenient for local development or very small deployments, but in production a separate Beat process is preferred.

```bash
python manage.py runcelery -B
```

---

### Run Celery worker (options)

Default (no options):

```bash
python manage.py runcelery
```

Worker options (Celery 5.x worker CLI):

| Option | Short | Description | Example |
|--------|-------|--------------|---------|
| `--concurrency` | `-c` | Number of worker processes (default: CPU count) | `-c 4` |
| `--pool` | `-P` | Pool type: `prefork`, `eventlet`, `gevent`, `solo`, `threads` | `-P threads` |
| `--queues` | `-Q` | Comma-separated queue names to consume | `-Q default,high` |
| `--loglevel` | `-l` | Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL | `-l DEBUG` |
| `--hostname` | `-n` | Custom worker hostname | `-n worker1@%h` |
| `--autoscale` | | Autoscale workers (max,min) | `--autoscale 10,3` |
| `--beat` | `-B` | Run beat scheduler in the same process | `-B` |
| `--logfile` | `-f` | Log to file instead of stderr | `-f celery.log` |

Examples:

```bash
# 4 worker processes, prefork pool (default)
python manage.py runcelery -c 4

# Thread pool with 8 threads
python manage.py runcelery -P threads -c 8

# Consume only 'default' and 'high' queues
python manage.py runcelery -Q default,high

# Debug logging
python manage.py runcelery -l DEBUG

# Autoscale between 3 and 10 workers
python manage.py runcelery --autoscale 10,3

# Run worker and beat together (dev/simple only)
python manage.py runcelery -B
```

### Run Celery Beat only (scheduler)

| Option | Short | Description | Example |
|--------|-------|--------------|---------|
| `--schedule` | `-s` | Path to schedule database (default: `celerybeat-schedule`) | `-s /var/run/celery/beat-schedule` |
| `--loglevel` | `-l` | Log level | `-l INFO` |
| `--logfile` | `-f` | Log file path | `-f beat.log` |
| `--pidfile` | | PID file (for daemon/process managers) | `--pidfile /var/run/celery/beat.pid` |
| `--max-interval` | | Max seconds between schedule iterations | `--max-interval 300` |

Example:

```bash
python manage.py runbeat -l INFO -s celerybeat-schedule
```

## Migrations (Django-like, Aerich)

Migration files live at **project root** in **`migrations/<app_label>/`** (e.g. **`migrations/user/`**, **`migrations/posts/`**). They are **not** inside each app (e.g. not in `apps/user/migrations/`). Use the app **label** (the last part of the app path), e.g. `user` for `apps.user`.

After `python manage.py makemigrations user`, look for new files in **`migrations/user/`** at the project root.

**First time (including after clone):** run `makemigrations` for each app that has models, then `migrate`. No separate init command.

### Create migrations

When an app has no migrations yet (first time or new app), or when you change models (add/remove fields or models):

1. **Create migration** for that app:

   ```bash
   python manage.py makemigrations <app_label>
   ```

   Examples:

   ```bash
   python manage.py makemigrations user
   python manage.py makemigrations user --name add_email_index
   ```

   If the app has no migrations yet, this creates the first migration in `migrations/<app_label>/`. Otherwise it generates a new migration file for your model changes.

2. **Apply all migrations** (all apps):

   ```bash
   python manage.py migrate
   ```

   To mark migrations as applied without running SQL (e.g. after applying them manually):

   ```bash
   python manage.py migrate --fake
   ```

### Show migration history

```bash
python manage.py showmigrations              # all apps
python manage.py showmigrations user        # one app
```

### After cloning the repo

1. Install dependencies and set up `.env`.
2. Run migrations for each app that has models (e.g. `user`):
   ```bash
   python manage.py makemigrations user
   python manage.py migrate
   ```
   If the repo already includes committed migration files in `migrations/user/`, you only need:
   ```bash
   python manage.py migrate
   ```

### New app

After `python manage.py startapp myapp` and adding `apps.myapp` to `INSTALLED_APPS`:

1. Run `python manage.py makemigrations myapp` (creates first migration in `migrations/myapp/`).
2. Run `python manage.py migrate`.

Configuration is in `pyproject.toml` under `[tool.aerich]` (location `migrations/`). Aerich is the migration tool for Tortoise ORM; see [Aerich](https://github.com/tortoise/aerich) for more options (e.g. `downgrade`).

## Environment

Copy `env.example` to `.env` and set:

- `FASTAPI_ENV` (development / production)
- `DATABASE_URL` (default: `sqlite://db.sqlite3`)
- `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`, `REDIS_URL`
- `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_ACCESS_EXPIRE_MINUTES` (for auth)
