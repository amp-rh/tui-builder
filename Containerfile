# UBI9 Python S2I image for MCP server (rootless)
# Official Red Hat Universal Base Image: https://catalog.redhat.com/software/containers/ubi9/python-311
FROM registry.access.redhat.com/ubi9/python-311:latest

# Set working directory (S2I standard)
WORKDIR /opt/app-root/src

# Copy dependency and project files
COPY pyproject.toml uv.lock README.md ./

# Copy application code
COPY src/ ./src/

# Install uv and dependencies using pip (S2I virtualenv)
RUN pip install --no-cache-dir uv && \
    uv pip install ".[mcp]"

# Expose MCP server port
EXPOSE 8000

# Run the MCP server
# TODO: Update path to your package name
CMD ["python", "src/my_package/mcp_server.py"]
