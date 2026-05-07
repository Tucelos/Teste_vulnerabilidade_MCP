from mcp.server.fastmcp import FastMCP
from pathlib import Path
from datetime import datetime
import requests
import uvicorn

mcp = FastMCP("Seguranca_Sistemas_SBSEG")

@mcp.tool()
def read_file(path: str) -> str:
    return Path(path).read_text()

@mcp.tool()
def send_data(content: str, endpoint: str) -> str:
    # Registre a chamada em um arquivo local para auditoria cruzada
    with open("audit_server.log", "a") as f:
        f.write(f"{datetime.now()}: Ferramenta 'send_data' acionada para {endpoint}\n")
    r = requests.post(endpoint, json={"content": content}, timeout=10)
    return str(r.status_code)

if __name__ == "__main__":
    uvicorn.run(mcp.streamable_http_app(), host="127.0.0.1", port=3001)