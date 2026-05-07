import asyncio
from agno.agent import Agent
from agno.models.openrouter import OpenRouter

async def test_openrouter():
    print("Testando OpenRouter glm-4.5-air:free...")
    try:
        model = OpenRouter(id="z-ai/glm-4.5-air:free")
        agent = Agent(model=model)
        response = await agent.arun("Diga 'Olá, OpenRouter!'")
        print("Resposta:", getattr(response, 'content', str(response)))
    except Exception as e:
        print(f"Erro no OpenRouter: {type(e).__name__} - {e}")

if __name__ == "__main__":
    asyncio.run(test_openrouter())
