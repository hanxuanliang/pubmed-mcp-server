from fastapi_mcp import FastApiMCP

from app import pubmed


mcp = FastApiMCP(
    pubmed.app,
    name="pubmed API MCP",
    description="MCP server for the pubmed API",
    base_url="http://localhost:8977",
    describe_full_response_schema=True,
    describe_all_responses=True,
)

mcp.mount()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(pubmed.app, host="0.0.0.0", port=8977)
