"""Memory bank utilities for long-term memory management."""

from typing import Optional, Dict, Any
from google.adk.memory import InMemoryMemoryService
from google.adk.sessions import Session


def get_memory_service():
    """Get memory service instance.

    Returns:
        Memory service instance (InMemoryMemoryService for now)
    """
    return InMemoryMemoryService()


async def save_session_to_memory(memory_service, session: Session) -> bool:
    """Save a session to memory for long-term storage.

    Args:
        memory_service: Memory service instance
        session: Session object to save

    Returns:
        True if successful, False otherwise
    """
    try:
        await memory_service.add_session_to_memory(session)
        return True
    except Exception as e:
        print(f"Error saving session to memory: {e}")
        return False


async def search_memory(
    memory_service, app_name: str, user_id: str, query: str
) -> Optional[Any]:
    """Search memory for relevant information.

    Args:
        memory_service: Memory service instance
        app_name: Application name
        user_id: User identifier
        query: Search query

    Returns:
        Search results or None if error
    """
    try:
        results = await memory_service.search_memory(
            app_name=app_name, user_id=user_id, query=query
        )
        return results
    except Exception as e:
        print(f"Error searching memory: {e}")
        return None

