from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
from pydantic import BaseModel

from src.common.error_handler import BaseErrorHandler


class GreetingAgent(BaseModel):
    """Greeting Agent example"""

    async def invoke(self) -> str:
        return "Hello World from A2A"


class GreetingAgentExecutor(AgentExecutor):

    def __init__(self):
        self.agent = GreetingAgent()
        self.error_handler = BaseErrorHandler(
            component_name="GoodAgentExecutor",
            exit_on_error=False,  # don't kill the server on executor error
        )

    async def execute(self, context: RequestContext, event_queue: EventQueue):
        """Safe execution wrapper."""

        async def _run():
            result = await self.agent.invoke()
            await event_queue.enqueue_event(new_agent_text_message(result))

        # use ASYNC handler here
        return await self.error_handler.handle_async(_run)

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        raise Exception("cancel not supported")
