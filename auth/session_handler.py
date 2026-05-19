"""
Session Handler — manages user authentication sessions.
Handles session creation, validation, and expiry.
"""
import hashlib
import time
import uuid
from typing import Optional

SESSION_EXPIRY_SECONDS = 3600  # 1 hour


class SessionStore:
    def __init__(self):
        self._sessions: dict[str, dict] = {}

    def create_session(self, user_id: str) -> str:
        """Create a new session for a user and return the session token."""
        session_id = str(uuid.uuid4())
        token = hashlib.sha256(f"{user_id}{session_id}{time.time()}".encode()).hexdigest()
        self._sessions[token] = {
            "user_id": user_id,
            "created_at": time.time(),
            "last_seen": time.time(),
        }
        return token

    def validate_session(self, token: str) -> Optional[str]:
        """Validate a session token and return the user_id if valid."""
        session = self._sessions.get(token)
        if not session:
            return None
        if time.time() - session["created_at"] > SESSION_EXPIRY_SECONDS:
            del self._sessions[token]
            return None
        session["last_seen"] = time.time()
        return session["user_id"]

    def revoke_session(self, token: str) -> bool:
        """Revoke an active session."""
        if token in self._sessions:
            del self._sessions[token]
            return True
        return False

    def cleanup_expired(self) -> int:
        """Remove all expired sessions. Returns count removed."""
        now = time.time()
        expired = [t for t, s in self._sessions.items()
                   if now - s["created_at"] > SESSION_EXPIRY_SECONDS]
        for token in expired:
            del self._sessions[token]
        return len(expired)
