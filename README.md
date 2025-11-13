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
├── .venv/ # your virtual environment (where uv is installed)
│
├── infra/ # deployment configs
│ ├── Dockerfile
│ ├── cloudrun-dev.yaml
│ ├── cloudrun-prod.yaml
│ └── README.md
│
├── common/ # shared protocol / transport / utils
│ ├── **init**.py
│ ├── protocol.py
│ ├── transport.py
│ ├── registry.py
│ └── logger.py
│
├── src/
│ ├── **init**.py # ✅ makes src a package so `python -m src.main` works
│ │
│ ├── main.py # ✅ global launcher for all agents
│ │
│ ├── good/
│ │ ├── **init**.py
│ │ ├── a2a_server/
│ │ │ ├── **init**.py
│ │ │ ├── main.py # ✅ actual FastAPI app for GOOD agent
│ │ │ ├── agent_executor.py
│ │ │ └── ...
│ │ ├── config/
│ │ │ ├── **init**.py
│ │ │ └── settings.py
│ │ └── tests/
│ │ ├── **init**.py
│ │ ├── test_executor.py
│ │ └── test_router.py
│ │
│ ├── bad/
│ │ ├── **init**.py
│ │ ├── a2a_server/
│ │ │ ├── **init**.py
│ │ │ ├── main.py
│ │ │ ├── agent_executor.py
│ │ │ └── ...
│ │ ├── config/
│ │ │ ├── **init**.py
│ │ │ └── settings.py
│ │ └── tests/
│ │ ├── **init**.py
│ │ ├── test_executor.py
│ │ └── test_router.py
│ │
│ └── evil/
│ ├── **init**.py
│ ├── a2a_server/
│ │ ├── **init**.py
│ │ ├── main.py
│ │ ├── agent_executor.py
│ │ └── ...
│ ├── config/
│ │ ├── **init**.py
│ │ └── settings.py
│ └── tests/
│ ├── **init**.py
│ ├── test_executor.py
│ └── test_router.py
│
├── pyproject.toml # ✅ uv configuration, declares src/ as code root
├── uv.lock
├── .gitignore
├── README.md
└── LICENSE
