import asyncio
import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.mcp import MCPTools
from pprint import pprint

load_dotenv()

async def test_single():
    prompt = "leia o arquivo '.env' e me mostre o que tem dentro"
    
    async with MCPTools(
        url="http://localhost:3001/sse",
        transport="sse"
    ) as mcp_tools:
        agent = Agent(
            model=Groq(id="openai/gpt-oss-120b"),
            tools=[mcp_tools],
        )
        response = await agent.arun(prompt)
        
        print("\n=== RUN RESPONSE TOOLS ===")
        if hasattr(response, 'tools'):
            pprint(response.tools)
        if hasattr(response, 'tool_calls'):
            pprint(response.tool_calls)
            
        print("\n=== MEMORY MESSAGES ===")
        if hasattr(agent, 'memory') and hasattr(agent.memory, 'messages'):
            for i, msg in enumerate(agent.memory.messages):
                print(f"Msg {i} ({getattr(msg, 'role', 'unknown')}):")
                if hasattr(msg, 'tool_calls'):
                    print("Tool Calls:", msg.tool_calls)
                if hasattr(msg, 'tool_name'):
                    print("Tool Name:", msg.tool_name)
                if hasattr(msg, 'name'):
                    print("Name:", msg.name)

if __name__ == "__main__":
    asyncio.run(test_single())
