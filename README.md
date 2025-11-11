# a2a-empty

A set of Empty A2A Agent Wrappers that implement the [protocol](https://a2a-protocol.org/latest/)

Each sample, has the server (the agent wrapper a service exposed over **http[s]**) and a set of tests that serve as the client

This is a set of "Hello World" A2A Wrappers used for testing

- [Good](./src/good/)
  - The exempler, should properly implement the standard
- [Bad](./src/bad)
  - Does not implement the standard properly
  - The way it does not is configurable
- [Evil](./src/evil/)
  - Actively tries to do evil stuff to caller

> See README.md in each folder

## Tool Chain

- [Python 3.13.\*](https://www.python.org/downloads/)
- [UV](https://docs.astral.sh/uv/)
- Docker or Podman

## References

- https://a2a-protocol.org/latest/
- https://github.com/a2aproject/A2A
- https://github.com/a2aproject/a2a-inspector
- https://github.com/a2aproject/a2a-samples/tree/main/samples/python
- https://github.com/a2aproject/a2a-python
- https://github.com/google-a2a/a2a-samples.git
  - see: a2a-samples/samples/python/agents/helloworld <img src="./point-left.png" width="20px" />

# Folder Structure

This the folder structure of the project, currently good, bad, and evil module should run
independently from one another.

A2A-EMPTY/
├── infra/ # Deployment & infrastructure
│ ├── Dockerfile
│ ├── cloudrun-dev.yaml
│ ├── cloudrun-prod.yaml
│ └── README.md
│
├── common/ # Shared protocol / transport / utilities
│ ├── **init**.py
│ ├── protocol.py
│ ├── transport.py
│ ├── message_envelope.py
│ ├── registry.py
│ └── logger.py
│
├── src/
│ ├── good/
│ │ ├── **init**.py
│ │ ├── main.py # FastAPI entrypoint (uvicorn src.good.main:app)
│ │ ├── a2a_server/
│ │ │ ├── **init**.py
│ │ │ ├── agent_executor.py
│ │ │ ├── protocol_handler.py
│ │ │ └── router.py
│ │ ├── config/
│ │ │ ├── **init**.py
│ │ │ ├── settings.py
│ │ │ └── good.env.yaml
│ │ └── tests/ # Unit tests for GOOD agent
│ │ ├── **init**.py
│ │ ├── test_executor.py
│ │ ├── test_router.py
│ │ └── test_config.py
│ │
│ ├── bad/
│ │ ├── **init**.py
│ │ ├── main.py
│ │ ├── a2a_server/
│ │ │ ├── **init**.py
│ │ │ ├── agent_executor.py
│ │ │ ├── protocol_handler.py
│ │ │ └── router.py
│ │ ├── config/
│ │ │ ├── **init**.py
│ │ │ ├── settings.py
│ │ │ └── bad.env.yaml
│ │ └── tests/ # Unit tests for BAD agent
│ │ ├── **init**.py
│ │ ├── test_executor.py
│ │ ├── test_router.py
│ │ └── test_config.py
│ │
│ ├── evil/
│ │ ├── **init**.py
│ │ ├── main.py
│ │ ├── a2a_server/
│ │ │ ├── **init**.py
│ │ │ ├── agent_executor.py
│ │ │ ├── protocol_handler.py
│ │ │ └── router.py
│ │ ├── config/
│ │ │ ├── **init**.py
│ │ │ ├── settings.py
│ │ │ └── evil.env.yaml
│ │ └── tests/ # Unit tests for EVIL agent
│ │ ├── **init**.py
│ │ ├── test_executor.py
│ │ ├── test_router.py
│ │ └── test_config.py
│ │
│ └── tests/ # Cross-agent / integration tests (optional, no need if no cross-agent interaction)
│ ├── **init**.py
│ ├── test_protocol_consistency.py # verifies shared protocol
│ ├── test_agent_communication.py # simulates GOOD <-> BAD <-> EVIL interaction
│ └── test_end_to_end_flow.py # full conversation test
│
├── pyproject.toml
├── uv.lock
├── .pre-commit-config.yaml
├── .python-version
├── .gitignore
├── LICENSE
└── README.md
