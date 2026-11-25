import os

import pytest
from sqlalchemy.engine import make_url

# Tests only ever use the local Docker database, never Neon.
DEFAULT_TEST_DATABASE_URL = "postgresql+psycopg://minos:minos@localhost:5433/minos"


def pytest_configure(config: pytest.Config) -> None:
    """Point the app at the test database, and refuse to run against Neon.

    TEST_DATABASE_URL defaults to Docker Postgres. It also replaces
    DATABASE_URL, so a Neon value loaded from .env never reaches a test.

    Raises:
        pytest.UsageError: If TEST_DATABASE_URL points at a neon.tech host.
    """
    url = os.environ.get("TEST_DATABASE_URL", DEFAULT_TEST_DATABASE_URL)
    host = make_url(url).host or ""
    if host == "neon.tech" or host.endswith(".neon.tech"):
        raise pytest.UsageError(
            f"TEST_DATABASE_URL points at Neon ({host}). Tests must use the "
            "local Docker database. Unset it or point it at localhost:5433."
        )
    os.environ["DATABASE_URL"] = url
