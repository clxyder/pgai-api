# Gen AI LLM API

API (Fastapi application) to explore Generative AI and Large Language Models using Ollama.

## Features
- Retrieval Augmented Generation (RAG)

## Requirements

- Python 3.12
- Fastapi
- Postgres as vector database ([pgai](https://www.timescale.com/blog/pgai-giving-postgresql-developers-ai-engineering-superpowers))
- Pytest
- Docker

## Installation

### Clone Project

```sh
git clone https://github.com/taiyeoguns/gen-ai-llm-api.git
```

### Add details in `.env` file

Create `.env` file from example file and maintain necessary details in it.

```sh
cp .env.example .env
```

The following environment variables should be set in the `.env` file even if they do not 'exist', the docker postgres image will use them for setting up the container -
`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`.

`OLLAMA_GENERATION_MODEL` and `OLLAMA_EMBEDDING_MODEL` should be set to values that exist in the [Ollama Registry](https://ollama.com/library) for generation model and embedding model respectively. For example, you can set `OLLAMA_GENERATION_MODEL` to `llama3.2:1b` and `OLLAMA_EMBEDDING_MODEL` to `nomic-embed-text`.


### Run application with Docker

It is advisable to run the entire application with Docker to ensure all components needed are set up correctly. Ensure database details are added to `.env` file from earlier.

**Note**: Make sure system to run application has adequate resources e.g. CPU, GPU to run the models.

To run the application with GPU support, install NVIDIA container toolkit from here: https://hub.docker.com/r/ollama/ollama

Also update the `docker-compose.yml` file, `ollama_service` section with:

```yaml
deploy:
    resources:
    reservations:
        devices:
        - driver: nvidia
        capabilities: ["gpu"]
        count: all
```

Full `ollama_service` in docker compose file will look like:

```yaml
ollama_service:
    container_name: ollama_container
    build:
      context: ./.docker/ollama
    ports:
      - "11434:11434"
    deploy:
      resources:
        reservations:
          devices:
          - driver: nvidia
            capabilities: ["gpu"]
            count: all
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:11434"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - ollama_data:/root/.ollama
```

With Docker and Docker Compose set up, run:

```sh
make docker-run
```

Thereafter, application should be available at `http://localhost:8000`

OpenAPI documentation page should also be available at `http://localhost:8000/docs`

## Retrieval Augmented Generation (RAG)

To test the RAG implementation, create new page content by navigating to `/pages/create` in the browser or send a `POST` request to the API endpoint `/v1/pages`.

After creating page content, test the chat with the AI model by sending a `POST` HTTP request to the `/v1/chat` endpoint and ask questions about the created content.


### Tests

In command prompt, run:

```sh
make test
```
