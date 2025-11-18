# TODO: revisit test not working
# import pytest
# from a2a.server.apps import A2AStarletteApplication
# from a2a.server.request_handlers import DefaultRequestHandler
# from a2a.server.tasks import InMemoryTaskStore
# from a2a.types import AgentCapabilities, AgentCard, AgentSkill
# from starlette.testclient import TestClient

# from ...src.good.a2a_server.agent_executor import GreetingAgentExecutor

# @pytest.fixture
# def test_app():
#     skill = AgentSkill(
#         id="hello_world",
#         name="Greet",
#         description="Returns a greeting",
#         tags=["greeting", "hello", "world"],
#         examples=["Hey", "Hello", "Hi"],
#     )

#     agent_card = AgentCard(
#         name="Greeting Agent",
#         description="Just a greeting agent",
#         url="http://localhost:9999/",
#         version="1.0.0",
#         default_input_modes=["text"],
#         default_output_modes=["text"],
#         capabilities=AgentCapabilities(),
#         skills=[skill],
#     )

#     app = A2AStarletteApplication(
#         http_handler=DefaultRequestHandler(
#             agent_executor=GreetingAgentExecutor(),
#             task_store=InMemoryTaskStore(),
#         ),
#         agent_card=agent_card,
#     ).build()

#     return TestClient(app)


# def test_greeting_response(test_app):
#     response = test_app.post("/a2a", json={"input": "Hello"})
#     assert response.status_code == 200
#     assert "Hello World from A2A" in response.json()["output"]
