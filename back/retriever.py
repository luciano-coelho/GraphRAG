import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_community.graphs import Neo4jGraph
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_ollama import OllamaLLM

load_dotenv()

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

def carregar_prompt(caminho_relativo="utils/prompt.txt"):
    base_dir = Path(__file__).parent  # back/
    caminho_completo = base_dir / caminho_relativo
    with open(caminho_completo, encoding="utf-8") as f:
        return PromptTemplate.from_template(f.read())

QA_PROMPT = carregar_prompt()

graph = Neo4jGraph(
    url=URI,
    username=USER,
    password=PASSWORD
)

llm = OllamaLLM(model=OLLAMA_MODEL)

chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    return_intermediate_steps=True,
    allow_dangerous_requests=True,
    verbose=False,
    qa_prompt=QA_PROMPT
)

def responder_pergunta(pergunta):
    resultado = chain.invoke({"query": pergunta})
    resposta = resultado.get("result", "").strip()

    if resposta and resposta.lower() != "[]" and "nenhuma informação" not in resposta.lower():
        return resposta

    passos = resultado.get("intermediate_steps", [])
    cypher_result = next((s.get("cypher_result") for s in passos if "cypher_result" in s), None)

    if not cypher_result:
        return "Nenhuma informação relevante encontrada."

    linhas = ["Ativos encontrados:"]
    for item in cypher_result:
        ativo = item.get("a", {})
        relacao = item.get("r", {})

        nome = ativo.get("nome")
        if nome:
            linhas.append(f"* {nome}")
            detalhes = [f"  - {k.capitalize()}: {v}" for k, v in ativo.items() if k != "nome"]
            linhas.extend(detalhes)

        valor = relacao.get("valor_investido")
        if valor:
            linhas.append(f"  - Valor investido: {valor}")

    return "\n".join(linhas)
