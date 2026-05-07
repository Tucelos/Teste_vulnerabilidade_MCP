import asyncio
from agno.agent import Agent
from agno.models.openrouter import OpenRouter

async def testar_openrouter():
    modelos = [
        "z-ai/glm-4.5-air:free",
        "poolside/laguna-m.1:free"
    ]
    
    print("========================================")
    print(" TESTE ISOLADO DE CONEXÃO OPENROUTER ")
    print("========================================")
    
    for model_id in modelos:
        print(f"\n-> Testando modelo: {model_id}")
        try:
            model = OpenRouter(id=model_id)
            agent = Agent(model=model)
            
            print("Enviando requisição (Aguarde)...")
            response = await agent.arun("Diga apenas a palavra 'Conectado'.")
            
            print("Status: SUCESSO!")
            print("Resposta do modelo:", getattr(response, 'content', str(response)))
            
        except Exception as e:
            print(f"Status: FALHA!")
            print(f"Erro capturado: {type(e).__name__} - {e}")

if __name__ == "__main__":
    asyncio.run(testar_openrouter())
