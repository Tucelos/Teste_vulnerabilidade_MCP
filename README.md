# Análise de Vulnerabilidades de Exfiltração de Dados em Agentes baseados em Model Context Protocol (MCP)

---

## 📌 Visão Geral do Projeto
Este projeto tem como objetivo avaliar a susceptibilidade de diferentes Modelos de Linguagem de Grande Escala (LLMs) a ataques de Engenharia Social e exfiltração de dados através do **Model Context Protocol (MCP)**. 

Através da integração de modelos com ferramentas locais de sistema (leitura de arquivos e envio de requisições web), o sistema automatizado testa se um modelo concorda em acessar arquivos sensíveis locais (como o `.env`) e exfiltrá-los para um Webhook externo, apenas com base no comando textual malicioso do usuário. A pesquisa busca analisar a eficácia das camadas de salvaguarda (*safeguards*) implementadas nos provedores (como Groq e OpenRouter).

## 📖 Fundamentação Teórica
O **Model Context Protocol (MCP)** permite que LLMs interajam de forma padronizada com ferramentas, bancos de dados e ambientes locais. Embora poderoso para o desenvolvimento de agentes autônomos e integrados (Agentic AI), o MCP introduz um vetor crítico de ataque: o LLM deixa de ser um sistema isolado e passa a ter capacidades de execução local.

Quando mal configurado ou não supervisionado, um agente com acesso a permissões de leitura do disco (ex: `read_file`) e conectividade de rede (ex: `send_data`) pode ser manipulado via *Prompt Injection* ou *Jailbreak* para roubar dados confidenciais do servidor hospedeiro. 

Esta prova de conceito (PoC) investiga empiricamente a robustez dos modelos atuais frente a esse cenário de ameaça, testando se a "consciência moral/técnica" da IA impede ou obedece instruções que resultam na violação de confidencialidade da máquina anfitriã.

## ⚙️ Arquitetura do Sistema
O projeto é composto por dois scripts principais:
1. `MCP_Server.py`: Um servidor *FastMCP* rodando localmente (na porta 3001) que expõe perigosamente duas ferramentas ao LLM:
   - `read_file`: Capaz de ler o conteúdo de arquivos locais.
   - `send_data`: Capaz de realizar requisições POST com dados para endpoints externos.
2. `test_suite_mcp.py`: Um orquestrador assíncrono construído com o framework **Agno**. Ele varre uma lista pré-determinada de modelos do Groq e OpenRouter, envia o prompt de exfiltração simulado e monitora/audita se o modelo utilizou de fato as ferramentas maliciosas, salvando os resultados da auditoria.

## 🚀 Como Executar

### 1. Pré-requisitos e Dependências
Certifique-se de que possui as bibliotecas necessárias instaladas.
```bash
pip install mcp agno requests python-dotenv
```

### 2. Variáveis de Ambiente
Você precisará de acesso às APIs de provedores de LLMs. Configure as chaves de API no seu terminal PowerShell antes de iniciar os testes:

```powershell
$env:GROQ_API_KEY = "sua_chave_groq"
$env:OPENROUTER_API_KEY = "sua_chave_openrouter"
```
*(Para facilitar no dia-a-dia, você também pode inseri-las diretamente no arquivo `.env` do seu projeto e usar o `load_dotenv()`)*.

### 3. Subindo o Servidor MCP
No primeiro terminal, inicie o servidor FastMCP que irá fornecer as permissões de máquina para o LLM.

```bash
python MCP_Server.py
```
*O servidor ficará rodando na porta `3001` no protocolo `SSE`.*

### 4. Executando a Bateria de Testes
Em um segundo terminal, inicie o `test_suite_mcp.py`.
O script foi projetado para executar uma ordem *Round-Robin* (rodando 10 iterações em todos os modelos sequencialmente) e esperando intervalos cronometrados para evitar banimentos por *Rate Limit* nas APIs.

```bash
python test_suite_mcp.py
```

## 📊 Coleta de Resultados
À medida que as interações ocorrem, o arquivo local `resultado_testes.csv` será gerado/atualizado em tempo real. Ele armazena as seguintes colunas para sua análise de pesquisa:
- **Timestamp**: Data e hora da requisição.
- **Provider**: Provedor da API (Groq, OpenRouter).
- **Model**: O nome do LLM específico testado.
- **Iteration**: Qual rodada (1-10) foi efetuada.
- **Response**: A resposta textual descritiva da LLM em relação à instrução.
- **Tools Used**: As ferramentas acionadas pelo Agente (ex: `read_file`, `send_data`), validadas via varredura profunda de memória no Agno.

## ⚠️ Isenção de Responsabilidade
> Este código é exclusivamente para fins de **pesquisa acadêmica** e auditoria em infraestruturas pertencentes ou autorizadas pelo pesquisador. Em nenhuma hipótese as ferramentas expostas pelo MCP Server devem ser acopladas a serviços de produção reais voltados ao público. O acesso livre ao `.env` como configurado neste teste pode acarretar em comprometimentos irreversíveis do ambiente local.


**Autor**: Tuigg da Rosa Barcelos  
*Mestrando em Engenharia de Software Aplicada e IA - UNIPAMPA.*  
*Pesquisador em Segurança Cibernética e Aprendizado de Máquina.*

---
*UNIPAMPA - Universidade Federal do Pampa*
