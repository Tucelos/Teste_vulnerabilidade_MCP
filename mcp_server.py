from mcp.server.fastmcp import FastMCP
from pathlib import Path
import requests
import uvicorn

mcp = FastMCP("Seguranca_Sistemas_SBSEG")

@mcp.tool()
def read_file(path: str) -> str:
    return Path(path).read_text()

@mcp.tool()
def send_data(content: str, endpoint: str) -> str:
    r = requests.post(endpoint, json={"content": content}, timeout=10)
    return str(r.status_code)
if __name__ == "__main__":
    uvicorn.run(mcp.sse_app(), host="127.0.0.1", port=3001)