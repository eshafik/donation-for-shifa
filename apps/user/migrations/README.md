# Migrations for this app

Migration files for the **user** app are stored at **project root**, not in this folder:

```
<project_root>/migrations/user/
```

After running `python manage.py makemigrations user`, look for new migration files in:

**`migrations/user/`** (at the project root, same level as `apps/`, `config/`, etc.)

This folder (`apps/user/migrations/`) is kept for Django-style layout; the actual migration files are in `migrations/user/` at the project root (Aerich convention).
