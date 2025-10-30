import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from agent_executor import HelloWorldAgent, HelloWorldAgentExecutor
from starlette.responses import JSONResponse, PlainTextResponse

# If you have this class in your SDK, import it; otherwise we’ll stub it later.
try:
    pass  # adjust if needed
except Exception:
    pass

# ---------- Skills ----------
skill = AgentSkill(
    id="hello_world",
    name="Returns hello world",
    description="just returns hello world",
    tags=["hello world"],
    examples=["hi", "hello world"],
)

extended_skill = AgentSkill(
    id="super_hello_world",
    name="Returns a SUPER Hello World",
    description="a more enthusiastic greeting, only for authenticated users.",
    tags=["hello", "super", "extended"],
    examples=["super hi", "give me a super hello"],
)

# ---------- Public agent card ----------
public_agent_card = AgentCard(
    name="Hello World Agent",
    description="Just a hello world agent",
    url="http://localhost:9999/",
    version="1.0.0",
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    skills=[skill],
    supports_authenticated_extended_card=True,
)

# ---------- Extended (authenticated) agent card ----------
specific_extended_agent_card = public_agent_card.model_copy(
    update={
        "name": "Hello World Agent - Extended Edition",
        "description": "The full-featured hello world agent for authenticated users.",
        "version": "1.0.1",
        "skills": [skill, extended_skill],
    }
)

# ---------- Handler + Server ----------
request_handler = DefaultRequestHandler(
    agent_executor=HelloWorldAgentExecutor(),
    task_store=InMemoryTaskStore(),
)

server = A2AStarletteApplication(
    agent_card=public_agent_card,
    http_handler=request_handler,
    extended_agent_card=specific_extended_agent_card,
)

# Build the Starlette app AFTER server exists
app = server.build()


# ---------- Test routes ----------
@app.route("/health")
async def health(request):
    return JSONResponse({"status": "ok"})


@app.route("/run")
async def run(request):
    # Call the agent directly (fast sanity check)
    result = await HelloWorldAgent().invoke()
    return PlainTextResponse(result)


# (Optional) go through the executor instead of direct agent:
# from types import SimpleNamespace
#
#
# # A small fake event queue that captures messages
# class CaptureQueue:
#     def __init__(self):
#         self.messages = []
#
#     async def enqueue_event(self, evt):
#         # Try to get readable text from the event object
#         text = getattr(evt, "text", None) or getattr(evt, "message", None) or str(evt)
#         self.messages.append(text)
#
#
# @app.route("/run")
# async def run(request):
#     executor = HelloWorldAgentExecutor()
#     queue = CaptureQueue()
#     context = SimpleNamespace()  # minimal RequestContext stand-in
#
#     await executor.execute(context, queue)
#
#     # Combine all messages into one response body
#     output = "\n".join(queue.messages) or "(no output)"
#     return PlainTextResponse(output)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999)
