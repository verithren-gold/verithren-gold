from typing import List, Optional

#from mcp.server.fastmcp import FastMCP, Context

from fastmcp import FastMCP

from log_moment import ensure_daily_note, append_moment, get_today_path

# Name of our MCP server
mcp = FastMCP("curo-robin-bridge")


@mcp.tool()
async def log_moment_tool(
    ctx,
    title: str,
    body: str,
    tags: Optional[List[str]] = None,
    links: Optional[List[str]] = None,
) -> str:
    """
    Log a Curo & Robin moment into today's Obsidian daily note.
    """
    daily_path, date_str = get_today_path()
    ensure_daily_note(daily_path, date_str)
    append_moment(daily_path, title, body, tags, links)
    return f"Logged moment to {daily_path}"


if __name__ == "__main__":
    try:
        # Run as an HTTP server on localhost:8000
        mcp.run(transport="http", host="127.0.0.1", port=8000)
    except KeyboardInterrupt:
        pass



