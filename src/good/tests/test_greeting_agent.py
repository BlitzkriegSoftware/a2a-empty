import asyncio

from ..a2a_server.agent_executor import GreetingAgent


def test_greeting_agent_invokes_correctly():
    agent = GreetingAgent()
    result = asyncio.run(agent.invoke())
    assert result == "Hello World from A2A"
