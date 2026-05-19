"""
Database Configuration Loader — reads database settings from environment.
Supports PostgreSQL, MySQL, and SQLite connection profiles.
"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class DatabaseConfig:
    host: str
    port: int
    name: str
    user: str
    password: str
    ssl_mode: str = "require"
    pool_size: int = 10
    max_overflow: int = 5

    @property
    def dsn(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


def load_database_config(env_prefix: str = "DB") -> DatabaseConfig:
    """
    Load database configuration from environment variables.
    Expected vars: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
    """
    def require(key: str) -> str:
        value = os.environ.get(f"{env_prefix}_{key}")
        if not value:
            raise EnvironmentError(f"Required env var {env_prefix}_{key} is not set")
        return value

    return DatabaseConfig(
        host=require("HOST"),
        port=int(os.environ.get(f"{env_prefix}_PORT", "5432")),
        name=require("NAME"),
        user=require("USER"),
        password=require("PASSWORD"),
        ssl_mode=os.environ.get(f"{env_prefix}_SSL_MODE", "require"),
        pool_size=int(os.environ.get(f"{env_prefix}_POOL_SIZE", "10")),
    )


def get_read_replica_config() -> Optional[DatabaseConfig]:
    """Return read replica config if configured, else None."""
    if not os.environ.get("DB_REPLICA_HOST"):
        return None
    return DatabaseConfig(
        host=os.environ["DB_REPLICA_HOST"],
        port=int(os.environ.get("DB_REPLICA_PORT", "5432")),
        name=os.environ.get("DB_NAME", ""),
        user=os.environ.get("DB_REPLICA_USER", os.environ.get("DB_USER", "")),
        password=os.environ.get("DB_REPLICA_PASSWORD", os.environ.get("DB_PASSWORD", "")),
    )
