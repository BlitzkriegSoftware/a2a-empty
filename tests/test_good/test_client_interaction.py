import uuid

import httpx
import pytest
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    Message,
    MessageSendParams,
    Part,
    Role,
    SendMessageRequest,
    TextPart,
)

BASE_URL = "http://localhost:9999"
PUBLIC_AGENT_CARD_PATH = "/.well-known/a2a-agent-card.json"


@pytest.mark.asyncio
async def test_client_can_send_message():
    async with httpx.AsyncClient() as httpx_client:
        resolver = A2ACardResolver(httpx_client=httpx_client, base_url=BASE_URL)
        agent_card = await resolver.get_agent_card()

        client = A2AClient(httpx_client=httpx_client, agent_card=agent_card)

        message_payload = Message(
            role=Role.user,
            message_id=str(uuid.uuid4()),
            parts=[Part(root=TextPart(text="Hello, how are you?"))],
        )
        request = SendMessageRequest(
            id=str(uuid.uuid4()),
            params=MessageSendParams(message=message_payload),
        )

        response = await client.send_message(request)
        assert response.parts[0].text == "Hello World from A2A"
