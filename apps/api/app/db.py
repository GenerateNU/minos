import os

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Parent class for every table. Alembic reads Base.metadata."""


def database_url() -> str:
    """Return DATABASE_URL, or fail loudly if it is missing.

    Locally it points at Docker Postgres (see .env.example). In deployment it
    is the Neon connection string with the scheme set to postgresql+psycopg://.
    """
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL is not set. Copy apps/api/.env.example to apps/api/.env "
            "and run commands with `uv run --env-file .env ...`."
        )
    return url
