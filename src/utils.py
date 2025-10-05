from __future__ import annotations

import os
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    # Imported only for type checking to avoid import-time overhead
    from sqlalchemy.engine import Engine

_engine: Optional["Engine"] = None


def get_engine() -> "Engine":
    global _engine
    if _engine is not None:
        return _engine

    # Defer heavy imports to reduce cold-start time
    from dotenv import load_dotenv
    from sqlalchemy import create_engine

    # Load environment variables only when needed
    load_dotenv()

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not set. Define it in the environment or .env file."
        )

    _engine = create_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        pool_recycle=1800,
        future=True,
    )
    return _engine


def db_connect() -> "Engine":
    # Backwards-compatible alias
    return get_engine()
