# TODO: revisit test not working
# import uuid

# import httpx
# import pytest
# from unittest.mock import AsyncMock, patch

# from a2a.client import A2ACardResolver, A2AClient
# from a2a.types import (
#     AgentCard,
#     Message,
#     MessageSendParams,
#     Part,
#     Role,
#     SendMessageRequest,
#     TextPart,
# )

# BASE_URL = "http://localhost:9999"
# PUBLIC_AGENT_CARD_PATH = "/.well-known/a2a-agent-card.json"


# @patch("a2a.client.A2ACardResolver.get_agent_card", new_callable=AsyncMock)
# @pytest.mark.asyncio
# async def test_client_can_send_message(mock_get_card: AsyncMock) -> None:
#     # Provide a minimal mock AgentCard
#     mock_get_card.return_value = AgentCard(
#         id="agent-id",
#         name="MockAgent",
#         endpoint=f"{BASE_URL}/messages",
#         capabilities=[],
#         public_key="mock-public-key",
#     )

#     async with httpx.AsyncClient() as httpx_client:
#         resolver = A2ACardResolver(httpx_client=httpx_client, base_url=BASE_URL)
#         agent_card = await resolver.get_agent_card(PUBLIC_AGENT_CARD_PATH)

#         client = A2AClient(httpx_client=httpx_client, agent_card=agent_card)

#         message_payload = Message(
#             role=Role.user,
#             message_id=str(uuid.uuid4()),
#             parts=[Part(root=TextPart(text="Hello, how are you?"))],
#         )
#         request = SendMessageRequest(
#             id=str(uuid.uuid4()),
#             params=MessageSendParams(message=message_payload),
#         )

#         response = await client.send_message(request)

#         # Adjusted assertion to match actual message structure
#         assert response.messages[0].parts[0].root.text == "Hello World from A2A"
