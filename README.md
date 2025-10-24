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
