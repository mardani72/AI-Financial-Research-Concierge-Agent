"""Main entry point for the Financial Research Agent."""

import asyncio
import os
import sys
from typing import Optional, Tuple
from google.adk.agents import LlmAgent
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.memory import InMemoryMemoryService
from google.genai import types
from agents.orchestrator_agent import create_orchestrator_agent
from memory.session_store import get_session_service
from memory.memory_bank import get_memory_service, save_session_to_memory
from config.settings import (
    GOOGLE_API_KEY,
    APP_NAME,
    DEFAULT_USER_ID,
    MEMORY_COMPACTION_INTERVAL,
    MEMORY_OVERLAP_SIZE,
)


# Set API key
if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY not found. Please set it in your .env file or environment.")
    sys.exit(1)

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


async def auto_save_to_memory(callback_context):
    """Automatically save session to memory after each agent turn."""
    try:
        await callback_context._invocation_context.memory_service.add_session_to_memory(
            callback_context._invocation_context.session
        )
    except Exception as e:
        print(f"Warning: Error auto-saving to memory: {e}")


def setup_agent_system() -> Tuple[Runner, str]:
    """Set up the complete agent system with sessions and memory.

    Returns:
        Tuple of (Runner instance, app_name)
    """
    # Create orchestrator agent
    orchestrator = create_orchestrator_agent()

    # Create App with context compaction
    # Note: Memory is handled automatically by the Runner's memory_service
    app = App(
        name=APP_NAME,
        root_agent=orchestrator,
        events_compaction_config=EventsCompactionConfig(
            compaction_interval=MEMORY_COMPACTION_INTERVAL,
            overlap_size=MEMORY_OVERLAP_SIZE,
        ),
    )

    # Set up session and memory services
    session_service = get_session_service(use_database=True)
    memory_service = get_memory_service()

    # Create runner
    runner = Runner(
        app=app,
        session_service=session_service,
        memory_service=memory_service,
    )

    return runner, APP_NAME


async def run_query(
    runner: Runner,
    app_name: str,
    query: str,
    user_id: str = DEFAULT_USER_ID,
    session_id: Optional[str] = None,
) -> None:
    """Run a query through the agent system.

    Args:
        runner: Runner instance
        app_name: Application name
        query: User query string
        user_id: User identifier
        session_id: Optional session ID (creates new if None)
    """
    if session_id is None:
        import uuid
        session_id = f"session_{uuid.uuid4().hex[:8]}"

    # Create or retrieve session
    session_service = runner.session_service
    try:
        session = await session_service.create_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )
    except Exception:
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )

    print(f"\n{'='*60}")
    print(f"Session: {session_id}")
    print(f"User > {query}")
    print(f"{'='*60}\n")

    # Create message content
    query_content = types.Content(role="user", parts=[types.Part(text=query)])

    # Run agent
    response_text = ""
    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session.id, new_message=query_content
        ):
            if event.is_final_response() and event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        response_text += part.text
                        print(part.text, end="", flush=True)

        print("\n")
    except ExceptionGroup as eg:
        print(f"\n\nError: TaskGroup exception occurred:")
        for i, exc in enumerate(eg.exceptions):
            print(f"  Exception {i+1}: {type(exc).__name__}: {exc}")
            import traceback
            traceback.print_exception(type(exc), exc, exc.__traceback__)
        raise
    except Exception as e:
        print(f"\n\nError: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exception(type(e), e, e.__traceback__)
        raise

    # Auto-save to memory
    try:
        await save_session_to_memory(runner.memory_service, session)
    except Exception as e:
        print(f"Warning: Could not save to memory: {e}")

    return response_text


async def interactive_mode(
    runner: Runner,
    app_name: str,
    initial_user_id: str = DEFAULT_USER_ID,
    initial_session_id: Optional[str] = None,
) -> None:
    """Run in interactive CLI mode.

    Args:
        runner: Runner instance
        app_name: Application name
        initial_user_id: User identifier to use for the session
        initial_session_id: Optional starting session ID
    """
    print("\n" + "="*60)
    print("Financial Research Agent - Interactive Mode")
    print("="*60)
    print("Enter your queries (type 'exit' to quit, 'new' for new session)\n")

    session_id = initial_session_id
    user_id = initial_user_id

    while True:
        try:
            query = input("Query > ").strip()

            if query.lower() == "exit":
                print("Goodbye!")
                break
            elif query.lower() == "new":
                session_id = None
                print("Started new session.\n")
                continue
            elif not query:
                continue

            await run_query(runner, app_name, query, user_id, session_id)

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


async def single_query_mode(
    runner: Runner,
    app_name: str,
    query: str,
    user_id: str = DEFAULT_USER_ID,
    session_id: Optional[str] = None,
) -> None:
    """Run a single query.

    Args:
        runner: Runner instance
        app_name: Application name
        query: User query string
        user_id: User identifier
        session_id: Optional session ID (creates new if None)
    """
    await run_query(runner, app_name, query, user_id=user_id, session_id=session_id)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Financial Research Agent - AI-powered equity research assistant"
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="Query to process (if not provided, runs in interactive mode)",
    )
    parser.add_argument(
        "--session-id",
        help="Session ID to use (creates new if not provided)",
    )
    parser.add_argument(
        "--user-id",
        default=DEFAULT_USER_ID,
        help=f"User ID (default: {DEFAULT_USER_ID})",
    )

    args = parser.parse_args()

    # Set up agent system
    print("Initializing Financial Research Agent...")
    runner, app_name = setup_agent_system()
    print("Agent system ready!\n")

    # Run query or interactive mode
    if args.query:
        asyncio.run(
            single_query_mode(
                runner,
                app_name,
                args.query,
                user_id=args.user_id,
                session_id=args.session_id,
            )
        )
    else:
        asyncio.run(
            interactive_mode(
                runner,
                app_name,
                initial_user_id=args.user_id,
                initial_session_id=args.session_id,
            )
        )


if __name__ == "__main__":
    main()

