#!/usr/bin/env python
import os
import subprocess
import sys
import click
import uvicorn
from fastapi import FastAPI

from config.celery import celery_app
from config.db import init_db
from config.settings import TORTOISE_ORM_CONFIG, INSTALLED_APPS, DEBUG

# Project root (where manage.py lives)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def _app_label(app_path: str) -> str:
    """Django-like app label from path: apps.user -> user."""
    return app_path.split(".")[-1]


def _run_aerich(args: list[str], check: bool = True) -> int:
    """Run aerich CLI from project root."""
    cmd = [sys.executable, "-m", "aerich"] + args
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    if check and result.returncode != 0:
        sys.exit(result.returncode)
    return result.returncode

APP_TEMPLATE = """
# {app_name}/__init__.py
# This file makes {app_name} a Python package
"""

MODELS_TEMPLATE = """
# {app_name}/models.py
from tortoise import fields, models


class ExampleModel(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    class Meta:
        default_connection = "default"
        table = "{app_name}_example"
"""

SCHEMAS_TEMPLATE = """
# {app_name}/schemas.py
from pydantic import BaseModel, ConfigDict


class ExampleCreate(BaseModel):
    name: str


class ExampleUpdate(BaseModel):
    name: str | None = None


class ExampleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
"""

ROUTES_TEMPLATE = """
# {app_name}/routes.py
from fastapi import APIRouter
from utils.response_wrapper import response_wrapper
from .views import example_view

router = APIRouter(prefix="/api/v1/{app_name}", tags=["{app_name}"])

router.get("/example", summary="Example endpoint")(response_wrapper(example_view))
"""

VIEWS_TEMPLATE = """
# {app_name}/views.py


async def example_view():
    return {{"message": "This is an example view"}}
"""

SERVICES_TEMPLATE = """
# {app_name}/services.py
# Add business logic here (e.g. CRUD using Tortoise models)
"""

TASKS_TEMPLATE = """
# {app_name}/tasks.py
from celery import shared_task


@shared_task
def example_task():
    return "This is an example task"
"""


@click.group()
def cli():
    pass


@click.command()
@click.argument('app_name')
@click.option('--register', is_flag=True, help='Append app to INSTALLED_APPS in config/settings.py')
def startapp(app_name, register):
    """Create a new app with the given name (Django-like: models, schemas, routes, views, services, tasks)."""
    app_dir = os.path.join('apps', app_name)
    os.makedirs(app_dir, exist_ok=True)

    files = {
        '__init__.py': APP_TEMPLATE.format(app_name=app_name),
        'models.py': MODELS_TEMPLATE.format(app_name=app_name),
        'schemas.py': SCHEMAS_TEMPLATE.format(app_name=app_name),
        'routes.py': ROUTES_TEMPLATE.format(app_name=app_name),
        'views.py': VIEWS_TEMPLATE.format(app_name=app_name),
        'services.py': SERVICES_TEMPLATE.format(app_name=app_name),
        'tasks.py': TASKS_TEMPLATE.format(app_name=app_name),
    }

    for filename, content in files.items():
        path = os.path.join(app_dir, filename)
        with open(path, 'w') as f:
            f.write(content)

    if register:
        settings_path = os.path.join(PROJECT_ROOT, "config", "settings.py")
        with open(settings_path, "r") as f:
            content = f.read()
        entry = f"apps.{app_name}"
        if entry not in content:
            content = content.replace(
                "INSTALLED_APPS = [",
                "INSTALLED_APPS = [\n    'apps." + app_name + "',"
            )
            with open(settings_path, "w") as f:
                f.write(content)
            click.echo(f"App 'apps.{app_name}' added to INSTALLED_APPS.")

    click.echo(f"App '{app_name}' created successfully! Add 'apps.{app_name}' to INSTALLED_APPS if not using --register.")
    click.echo(f"Then run: python manage.py makemigrations {app_name}  (creates first migration in migrations/{app_name}/)")


@click.command()
@click.option('--host', help='The host to bind to.')
@click.option('--port', default=8000, help='The port to bind to.')
def runserver(host, port):
    if DEBUG:
        host = host or '127.0.0.1'
        uvicorn.run("main:app", host=host, port=port, reload=True)
    else:
        host = host or '0.0.0.0'
        uvicorn.run("main:app", host=host, port=port, reload=False)


@click.command()
@click.option(
    "--concurrency", "-c",
    type=int,
    default=None,
    help="Number of child processes (default: number of CPUs). Use with -P prefork.",
)
@click.option(
    "--pool", "-P",
    type=click.Choice(["prefork", "eventlet", "gevent", "solo", "threads"], case_sensitive=False),
    default="prefork",
    help="Pool implementation (default: prefork). Use 'solo' for single-threaded, 'threads' for threading.",
)
@click.option(
    "--queues", "-Q",
    type=str,
    default=None,
    help="Comma-separated queue names to consume (e.g. default,high,low). Default: all queues.",
)
@click.option(
    "--loglevel", "-l",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "FATAL"], case_sensitive=False),
    default="INFO",
    help="Log level (default: INFO).",
)
@click.option(
    "--hostname", "-n",
    type=str,
    default=None,
    help="Set custom worker hostname (e.g. worker1@%%h).",
)
@click.option(
    "--autoscale",
    type=str,
    default=None,
    help="Enable autoscaling (e.g. '10,3' = max 10, min 3 workers).",
)
@click.option(
    "--beat", "-B",
    is_flag=True,
    default=False,
    help="Also run the Celery beat scheduler in the same process.",
)
@click.option(
    "--logfile", "-f",
    type=click.Path(),
    default=None,
    help="Log file path (default: stderr).",
)
def runcelery(concurrency, pool, queues, loglevel, hostname, autoscale, beat, logfile):
    """Run the Celery worker. Default: python manage.py runcelery. Pass options to customize."""
    argv = ["worker", f"--loglevel={loglevel}", f"--pool={pool}"]

    if concurrency is not None:
        argv.extend(["--concurrency", str(concurrency)])
    if queues:
        argv.extend(["--queues", queues])
    if hostname:
        argv.extend(["--hostname", hostname])
    if autoscale:
        argv.extend(["--autoscale", autoscale])
    if beat:
        argv.append("--beat")
    if logfile:
        argv.extend(["--logfile", logfile])

    celery_app.worker_main(argv)


@click.command()
@click.option(
    "--schedule", "-s",
    type=click.Path(),
    default=None,
    help="Path to the schedule database (default: celerybeat-schedule).",
)
@click.option(
    "--loglevel", "-l",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "FATAL"], case_sensitive=False),
    default="INFO",
    help="Log level (default: INFO).",
)
@click.option(
    "--logfile", "-f",
    type=click.Path(),
    default=None,
    help="Log file path (default: stderr).",
)
@click.option(
    "--pidfile",
    type=click.Path(),
    default=None,
    help="PID file path (useful when running as a daemon).",
)
@click.option(
    "--max-interval",
    type=int,
    default=None,
    help="Max seconds between schedule iterations.",
)
def runbeat(schedule, loglevel, logfile, pidfile, max_interval):
    """Run the Celery beat scheduler (separate process). Preferred in production."""
    beat_kwargs = {
        "loglevel": loglevel,
        "quiet": False,
    }
    if schedule is not None:
        beat_kwargs["schedule"] = schedule
    if logfile is not None:
        beat_kwargs["logfile"] = logfile
    if pidfile is not None:
        beat_kwargs["pidfile"] = pidfile
    if max_interval is not None:
        beat_kwargs["max_interval"] = max_interval
    celery_app.Beat(**beat_kwargs).run()


@click.command()
@click.argument('script_name')
def runscript(script_name):
    """Run a script with the FastAPI environment loaded."""
    import importlib.util

    async def run():
        await init_db(db_config=TORTOISE_ORM_CONFIG)
        # Load and execute the script
        script_path = os.path.join(PROJECT_ROOT, script_name)
        if not os.path.exists(script_path):
            click.echo(f"Script '{script_name}' not found.")
            sys.exit(1)

        spec = importlib.util.spec_from_file_location("script_module", script_path)
        script_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script_module)
        await script_module.main()
    run_async(run())


def _app_has_migrations(label: str) -> bool:
    """Return True if app has a migrations folder with at least one migration file (migrations/<label>/)."""
    migrations_dir = os.path.join(PROJECT_ROOT, "migrations", label)
    if not os.path.isdir(migrations_dir):
        return False
    for f in os.listdir(migrations_dir):
        if f.endswith(".py") and not f.startswith("__"):
            return True
    return False


@click.command()
@click.argument("app_name")
@click.option("--name", "-n", default=None, help="Migration name (e.g. add_email_field)")
def makemigrations(app_name, name):
    """Create a new migration for the given app (Django-like). Detects model/field changes."""
    label = app_name if "." not in app_name else _app_label(app_name)
    if label not in TORTOISE_ORM_CONFIG.get("apps", {}):
        click.echo(f"Unknown app '{app_name}'. Installed apps: {list(TORTOISE_ORM_CONFIG.get('apps', {}).keys())}")
        sys.exit(1)
    if not _app_has_migrations(label):
        click.echo(f"First migration for app '{label}' (init-db)...")
        _run_aerich(["--app", label, "init-db"])
    else:
        args = ["--app", label, "migrate"]
        if name:
            args.extend(["--name", name])
        _run_aerich(args)
    click.echo(f"Migration created for app '{label}'.")


@click.command()
@click.option("--fake", is_flag=True, help="Mark migrations as applied without running SQL")
def migrate(fake):
    """Apply all pending migrations for all apps (Django-like)."""
    for app_path in INSTALLED_APPS:
        label = _app_label(app_path)
        args = ["--app", label, "upgrade"]
        if fake:
            args.append("--fake")
        click.echo(f"Applying migrations for app '{label}'...")
        _run_aerich(args)
    click.echo("All migrations applied.")


@click.command()
@click.argument("app_name", required=False)
def showmigrations(app_name):
    """Show migration history (pending and applied)."""
    if app_name:
        label = app_name if "." not in app_name else _app_label(app_name)
        if label not in TORTOISE_ORM_CONFIG.get("apps", {}):
            click.echo(f"Unknown app '{app_name}'.")
            sys.exit(1)
        _run_aerich(["--app", label, "history"])
    else:
        for app_path in INSTALLED_APPS:
            label = _app_label(app_path)
            click.echo(f"--- {label} ---")
            _run_aerich(["--app", label, "history"])


cli.add_command(startapp)
cli.add_command(runserver)
cli.add_command(runcelery)
cli.add_command(runbeat)
cli.add_command(runscript)
cli.add_command(makemigrations)
cli.add_command(migrate)
cli.add_command(showmigrations)

if __name__ == '__main__':
    cli()
