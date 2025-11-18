# Simple A2A Agent Demo
## 1. Install dependencies

## 2. Run the Agent
Open a terminal and run the server with the dummy agent:

`uv run python -m src.main server --agent good`

The agent will be available at `http://localhost:9999`

## 3. Run the Client
Open a new terminal and run the test client:
cd to good/a2a_server and run:`uv run python -m src.main client --agent good`

## 4. Expected output:
showcasing the A2A protocol bare bones:
`Fetched public agent card successfully.
{
  "additionalInterfaces": null,
  "capabilities": {
    "extensions": null,
    "pushNotifications": null,
    "stateTransitionHistory": null,
    "streaming": null
  },`

## Reference:
https://www.youtube.com/watch?v=mFkw3p5qSuA <br>
https://a2a-protocol.org/latest/topics/key-concepts/#fundamental-communication-elements <br>
https://github.com/a2aproject/a2a-samples/tree/main/samples/python/agents/helloworld
