
from mcp.server.fastmcp import FastMCP

from server.engine import assess_message, next_steps

mcp = FastMCP(
    "HoldOn",
    stateless_http=True,
    json_response=True,
)


@mcp.tool()
def check_suspicious_message(message: str) -> dict:
    """Check a message for common scam warning signs."""
    return assess_message(message)


@mcp.tool()
def get_safe_next_steps(message: str) -> list[str]:
    """Analyze a message and return practical safety steps."""
    result = assess_message(message)
    return next_steps(result)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
