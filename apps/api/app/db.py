import os

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Parent class for every table. Alembic reads Base.metadata."""


def database_url() -> str:
    """Read the database URL from the environment.

    Locally it points at Docker Postgres or the Neon dev branch (see
    .env.example). In deployment it is the Neon connection string with the
    scheme set to postgresql+psycopg://.

    Returns:
        The value of DATABASE_URL.

    Raises:
        RuntimeError: If DATABASE_URL is not set.
    """
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL is not set. Copy apps/api/.env.example to apps/api/.env "
            "and run commands with `uv run --env-file .env ...`."
        )
    return url
