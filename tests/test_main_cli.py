from __future__ import annotations

from typing import Dict, List

import pytest

from src import main as launcher


def _make_call_tracker() -> Dict[str, List[str]]:
    """Helper to record which helper functions were called."""
    return {"server": [], "client": []}


def test_main_runs_server_with_explicit_agent(monkeypatch: pytest.MonkeyPatch) -> None:
    tracker = _make_call_tracker()

    def fake_run_server(agent: str) -> int:
        tracker["server"].append(agent)
        return 0

    def fake_run_client(agent: str) -> int:
        tracker["client"].append(agent)
        return 0

    monkeypatch.setattr(launcher, "run_server", fake_run_server)
    monkeypatch.setattr(launcher, "run_client", fake_run_client)

    exit_code = launcher.main(["server", "--agent", "good"])

    assert exit_code == 0
    assert tracker["server"] == ["good"]
    assert tracker["client"] == []


def test_main_runs_client_with_explicit_agent(monkeypatch: pytest.MonkeyPatch) -> None:
    tracker = _make_call_tracker()

    def fake_run_server(agent: str) -> int:
        tracker["server"].append(agent)
        return 0

    def fake_run_client(agent: str) -> int:
        tracker["client"].append(agent)
        return 0

    monkeypatch.setattr(launcher, "run_server", fake_run_server)
    monkeypatch.setattr(launcher, "run_client", fake_run_client)

    exit_code = launcher.main(["client", "--agent", "evil"])

    assert exit_code == 0
    assert tracker["server"] == []
    assert tracker["client"] == ["evil"]


def test_main_defaults_to_server_when_no_command(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tracker = _make_call_tracker()

    def fake_run_server(agent: str) -> int:
        tracker["server"].append(agent)
        return 0

    def fake_run_client(agent: str) -> int:
        tracker["client"].append(agent)
        return 0

    monkeypatch.setattr(launcher, "run_server", fake_run_server)
    monkeypatch.setattr(launcher, "run_client", fake_run_client)

    # No explicit command -> default "server", default agent from env ("good")
    exit_code = launcher.main([])

    assert exit_code == 0
    assert tracker["server"] == ["good"]
    assert tracker["client"] == []


def test_main_invalid_command_raises_system_exit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_run_server(agent: str) -> int:
        raise AssertionError("run_server should not be called")

    def fake_run_client(agent: str) -> int:
        raise AssertionError("run_client should not be called")

    monkeypatch.setattr(launcher, "run_server", fake_run_server)
    monkeypatch.setattr(launcher, "run_client", fake_run_client)

    # argparse will raise SystemExit with a non-zero code
    with pytest.raises(SystemExit) as exc_info:
        launcher.main(["invalid"])

    assert exc_info.value.code != 0
