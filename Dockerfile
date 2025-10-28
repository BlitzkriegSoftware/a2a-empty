FROM python:3.11-slim

# Use bash as the default shell so we can use `source` and other bash features
# (By default, Debian uses /bin/sh which doesn't support `source`)
SHELL ["/bin/bash", "-c"]

WORKDIR /app

# - `--no-install-recommends`: Keeps image size smaller by skipping optional packages

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \

    # Download and install `uv` from the official Astral script
    curl -Ls https://astral.sh/uv/install.sh | bash && \

    # Debug prints to verify where `uv` was installed
    echo "uv installed at: $(find /root/.local/bin -name uv)" && \
    echo "PATH before: $PATH" && \

    # Temporarily add `uv` to PATH for this RUN step
    export PATH="/root/.local/bin:$PATH" && \
    echo "PATH after: $PATH" && \

    # Verify that `uv` is working
    /root/.local/bin/uv --version && \

    # Clean up apt cache to reduce image size
    apt-get clean && rm -rf /var/lib/apt/lists/*


# Add uv to PATH permanently for all future Docker steps
ENV PATH="/root/.local/bin:$PATH"

COPY src/good/a2a-server/ /app

RUN uv venv && \
    source .venv/bin/activate && \
    uv sync --all-groups && \
    uv sync --upgrade

# Expose port 10003 so Docker knows which port the container serves traffic on
# Note: Port — just documents it for a test purpose. we will add the actual port 

EXPOSE 10003

# -----------------------------------------------------------------------------
# Default command to run the server when container starts. needs to modify
# - `uv run`: Executes the command inside the activated virtual environment. will remove this step and document it in readme. just for our understanding
# - `-m good.a2a-server`: Runs the module `good.a2a-server/.py`
# - `--host 0.0.0.0`: Binds to all network interfaces (needed for Docker/GCP). this is for test. will be changed
# - `--port 10003`: Runs the service on port 10003. this is for test. will be changed
# -----------------------------------------------------------------------------
CMD ["uv", "run", "python3", "-m", "good.a2a-server", "--host", "0.0.0.0", "--port", "10003"]
