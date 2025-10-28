# Desafio MBA Engenharia de Software com IA - Full Cycle

Descreva abaixo como executar a sua solução.

### Pré-requisitos

- Python 3.8 ou superior
- Ambiente virtual (recomendado)
- Variáveis de ambiente configuradas .env:
  - OPENAI_API_KEY: Sua chave de API da OpenAI
  - GEMINI_API_KEY: Sua chave de API do Gemini

### Instalação

1. Clone o repositório:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd mba-ia-desafio-ingestao-busca
   ```
3. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Execução

Crie arquivo .env na raiz do projeto com as variáveis de ambiente necessárias (veja o exemplo em .env.example).

Rodar docker-compose:

```bash
docker-compose up -d
```

Para iniciar a criação do índice de vetores, execute:

```bash
python src/ingest.py
```

Para iniciar o chat interativo, execute:

```bash
python src/chat.py
```

### Uso

Digite suas perguntas no prompt. Para sair, digite "sair", "exit" ou "quit".

### Estrutura do Projeto

- `src/ingest.py`: Script para ingestão e indexação de documentos.
- `src/chat.py`: Script para interação via chat com o modelo de linguagem.
