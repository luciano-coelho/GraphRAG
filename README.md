# Simple GraphRAG

Este projeto é um assistente de respostas financeiras baseado em grafo, utilizando Neo4j, LangChain e um modelo Ollama LLM (LLaMA 3). Ele permite responder perguntas sobre carteiras de investimento de clientes com base em um grafo estruturado de dados.

---

```text
simple-graphrag/
├── back/
│   ├── graph_setup.py            # Criação do grafo com dados JSON
│   ├── retriever.py              # Lógica principal de perguntas/respostas
│   ├── utils/
│   │   └── prompt.txt            # Prompt oficial usado no modo produção
│   └── data/
│       ├── customer.json         # Dados do cliente
│       └── assets.json           # Dados de ativos
├── test/
│   ├── retriever_test.py         # Runner de testes com perguntas
│   ├── questions.txt             # Lista de perguntas de teste
│   └── prompt_test.txt           # Prompt alternativo para testes
├── front/
│   └── app.py                    # Interface (ex: Streamlit)
├── .env                          # Variáveis de ambiente
├── docker-compose.yml           # Infraestrutura local com Neo4j
├── requirements.txt             # Dependências do projeto
```
### 1. Clone o projeto

```bash
git clone https://github.com/seu-usuario/simple-graphrag.git
cd simple-graphrag
```

### 2. Crie e ative o ambiente virtual

#### Linux/macOS:

```bash
python -m venv venv
source venv/bin/activate
```

#### Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o .env

Crie um arquivo `.env` na raiz com o seguinte conteúdo:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=suasenha
OLLAMA_MODEL=llama3
```

### 5. Suba o Neo4j com Docker

```bash
docker compose up --build```

### 6. Popule o grafo com os dados de exemplo

```bash
python back/graph_setup.py
```
## Como rodar os testes

Execute o script `retriever_test.py`, que lê as perguntas de `questions.txt` e utiliza o prompt `prompt_test.txt` para simular o comportamento do sistema:

```bash
python test/retriever_test.py
```

O resultado da IA será exibido diretamente no terminal para cada pergunta.

Se quiser adicionar mais perguntas, edite o arquivo:

```text
test/questions.txt
```

Ou, se quiser testar um prompt diferente, edite:

```text
test/prompt_test.txt
```
## Como executar com Streamlit

Execute a interface web com Streamlit usando o comando abaixo:

```bash
streamlit run front/app.py
```

Por padrão, a aplicação será aberta automaticamente no navegador em:

```
http://localhost:8501
```

Você poderá digitar suas perguntas e ver as respostas baseadas no grafo Neo4j.