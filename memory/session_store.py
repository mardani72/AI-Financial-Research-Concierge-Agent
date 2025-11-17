"""Session store utilities for managing user sessions."""

from typing import Optional, Dict, Any
from google.adk.sessions import DatabaseSessionService, InMemorySessionService
from config.settings import DB_URL, APP_NAME


def get_session_service(use_database: bool = True):
    """Get session service instance.

    Args:
        use_database: If True, use DatabaseSessionService, else InMemorySessionService

    Returns:
        Session service instance
    """
    if use_database:
        return DatabaseSessionService(db_url=DB_URL)
    else:
        return InMemorySessionService()


def create_user_session(
    session_service, user_id: str, session_id: str
) -> Optional[Any]:
    """Create or retrieve a user session.

    Args:
        session_service: Session service instance
        user_id: User identifier
        session_id: Session identifier

    Returns:
        Session object or None if error
    """
    try:
        session = session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )
        return session
    except Exception:
        # Session might already exist, try to get it
        try:
            session = session_service.get_session(
                app_name=APP_NAME, user_id=user_id, session_id=session_id
            )
            return session
        except Exception as e:
            print(f"Error creating/retrieving session: {e}")
            return None

