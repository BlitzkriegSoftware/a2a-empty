import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from src.common.error_handler import BaseErrorHandler
from src.common.logging import setup_logger

from .agent_executor import GreetingAgentExecutor

error_handler = BaseErrorHandler(component_name="GoodAgent", exit_on_error=True)
log_handler = setup_logger("GoodAgent")


def start_server() -> None:
    """Create and run the Greeting Agent server."""

    skill = AgentSkill(
        id="hello_world",
        name="Greet",
        description="Returns a greeting.",
        tags=["greeting", "hello", "world"],
        examples=["Hey", "Hello", "Hi"],
    )

    agent_card = AgentCard(
        name="Greeting Agent",
        description="Just a greeting agent",
        url="http://localhost:9999/",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(),
        skills=[skill],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=GreetingAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        http_handler=request_handler,
        agent_card=agent_card,
    )

    uvicorn.run(server.build(), host="0.0.0.0", port=9999)


def main() -> None:
    """Entry point for the Good agent with sync error handling."""
    log_handler.info("[GoodAgent] Starting server...")
    error_handler.handle(start_server)


if __name__ == "__main__":
    main()
