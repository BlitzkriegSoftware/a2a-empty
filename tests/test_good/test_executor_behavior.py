import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.good.a2a_server.agent_executor import GreetingAgentExecutor


def test_executor_enqueues_greeting():
    executor = GreetingAgentExecutor()
    mock_queue = MagicMock()
    mock_context = AsyncMock()

    asyncio.run(executor.execute(mock_context, mock_queue))

    mock_queue.enqueue_event.assert_called_once()
    args, _ = mock_queue.enqueue_event.call_args
    assert "Hello World from A2A" in args[0].parts[0].root.text


def test_executor_cancel_raises():
    executor = GreetingAgentExecutor()
    with pytest.raises(Exception, match="cancel not supported"):
        asyncio.run(executor.cancel(MagicMock(), MagicMock()))
