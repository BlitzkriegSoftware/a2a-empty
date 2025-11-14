import asyncio
import uuid
from typing import List, cast

import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    Message,
    MessageSendParams,
    Part,
    Role,
    SendMessageRequest,
    TextPart,
)

from src.common.error_handler import BaseErrorHandler
from src.common.logging import setup_logger

BASE_URL = "http://localhost:9999"
AGENT_CARD_PATH = "/.well-known/agent.json"

logger = setup_logger("GoodAgentClient")
error_handler = BaseErrorHandler(
    component_name="GoodAgentClient",
    exit_on_error=True,
)


async def run_client() -> None:
    """Async client that calls the GOOD agent using the A2A protocol."""

    logger.info(f"Connecting to {BASE_URL} ...")

    async with httpx.AsyncClient() as httpx_client:
        # ---------------------------------------------------------
        # 1. Fetch agent card
        # ---------------------------------------------------------
        logger.info("Fetching agent card...")

        resolver = A2ACardResolver(httpx_client=httpx_client, base_url=BASE_URL)

        agent_card = await resolver.get_agent_card(AGENT_CARD_PATH)
        logger.info("Agent card fetched successfully.")

        # ---------------------------------------------------------
        # 2. Initialize A2A client
        # ---------------------------------------------------------
        client = A2AClient(
            httpx_client=httpx_client,
            agent_card=agent_card,
        )
        logger.info("Client initialized successfully.")

        # ---------------------------------------------------------
        # 3. Build A2A message request
        # ---------------------------------------------------------
        part: Part = cast(Part, TextPart(text="Hello, how are you?"))
        parts: List[Part] = [part]

        message = Message(
            role=Role.user,
            message_id=str(uuid.uuid4()),
            parts=parts,
        )

        request = SendMessageRequest(
            id=str(uuid.uuid4()),
            params=MessageSendParams(message=message),
        )

        logger.info("Sending message to agent...")

        # ---------------------------------------------------------
        # 4. Send the message
        # ---------------------------------------------------------
        response = await client.send_message(request)

        # ---------------------------------------------------------
        # 5. Print response
        # ---------------------------------------------------------
        logger.info("Response received:")
        print(response.model_dump_json(indent=2))


async def main() -> None:
    await error_handler.handle_async(run_client)


if __name__ == "__main__":
    asyncio.run(main())
