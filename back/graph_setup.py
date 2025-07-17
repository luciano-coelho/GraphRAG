import os
import json
from neo4j import GraphDatabase
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

BASE_DIR = Path(__file__).resolve().parent
CUSTOMER_PATH = BASE_DIR / "utils" / "customer.json"
ASSETS_PATH = BASE_DIR / "utils" / "assets.json"

with open(CUSTOMER_PATH, encoding="utf-8") as f:
    customer = json.load(f)

with open(ASSETS_PATH, encoding="utf-8") as f:
    assets = json.load(f)

def create_graph(tx):
    tx.run("MATCH (n) DETACH DELETE n")

    query = """
    CREATE (c:Cliente {
        client_id: $client_id,
        nome: $nome,
        perfil_investidor: $perfil_investidor,
        email: $email
    })
    WITH c
    UNWIND $assets_data AS asset
    CREATE (a:Ativo {
        nome: asset.nome,
        tipo: asset.tipo,
        categoria: asset.categoria,
        risco: asset.risco
    })
    CREATE (c)-[:INVESTE_EM {
        valor_investido: asset.valor,
        data_aquisicao: asset.data
    }]->(a)
    """

    tx.run(query,
           **customer, 
           assets_data=assets)

with driver.session() as session:
    session.execute_write(create_graph)

driver.close()
print("Grafo criado com sucesso!")
