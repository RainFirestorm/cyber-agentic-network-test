"""
Deployment Startup Script — initializes services on container start.
Runs health checks, applies migrations, and starts the application.
"""
import os
import sys
import subprocess
import time


def wait_for_database(host: str, port: int, retries: int = 30) -> bool:
    """Poll until the database is reachable or retries exhausted."""
    import socket
    for attempt in range(retries):
        try:
            with socket.create_connection((host, port), timeout=2):
                print(f"[startup] Database ready at {host}:{port}")
                return True
        except OSError:
            print(f"[startup] Waiting for database... ({attempt + 1}/{retries})")
            time.sleep(2)
    return False


def run_migrations() -> bool:
    """Apply pending database migrations."""
    result = subprocess.run(
        ["python", "manage.py", "migrate", "--noinput"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"[startup] Migration failed:\n{result.stderr}")
        return False
    print("[startup] Migrations applied successfully")
    return True


def collect_static() -> None:
    """Collect static assets if in production mode."""
    if os.environ.get("DJANGO_ENV") == "production":
        subprocess.run(
            ["python", "manage.py", "collectstatic", "--noinput"],
            check=True, capture_output=True
        )
        print("[startup] Static files collected")


def main() -> int:
    db_host = os.environ.get("DB_HOST", "localhost")
    db_port = int(os.environ.get("DB_PORT", "5432"))

    if not wait_for_database(db_host, db_port):
        print("[startup] ERROR: Database did not become ready in time")
        return 1

    if not run_migrations():
        return 1

    collect_static()

    print("[startup] Startup complete — application ready")
    return 0


if __name__ == "__main__":
    sys.exit(main())
