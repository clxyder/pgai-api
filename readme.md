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

### Install Requirements

With a [virtualenv](https://virtualenv.pypa.io/) already set-up, install the requirements with pip:

```sh
make install
```

### Add details in `.env` file

Create `.env` file from example file and maintain necessary details in it.

```sh
cp .env.example .env
```

### Set up database

SQLAlchemy is used to model the data and alembic is used to keep the database up-to-date.

To setup a local db, fill in database details in `.env` file from earlier or set up environment variables. Ensure the database and user defined in `.env` is already created in Postgres.

For initial database setup, run the following commands:

```sh
make db-upgrade
```

Subsequently, after making any changes to the database models, run the following commands:

```sh
make db-migrate
make db-upgrade
```

### Run the application

Activate the virtual environment and start the application by running:

```sh
make run
```

### Tests

In command prompt, run:

```sh
make test
```

### Run application with Docker

Ensure database details are added to `.env` file from earlier.

The following environment variables should be set in the `.env` file even if they do not 'exist', the docker postgres image will use them for setting up the container -
`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`.

`OLLAMA_GENERATION_MODEL` and `OLLAMA_EMBEDDING_MODEL` should be set to values that exist in the [Ollama Registry](https://ollama.com/library) for generation model and embedding model respectively.

**Note**: Ensure system to run application has adequate resources e.g. CPU, GPU to run the models.

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

## Retrieval Augmented Generation (RAG)

To test the RAG implementation, create new page content by navigating to `/pages/create` in the browser or send a `POST` request to the API endpoint `/v1/pages`.

After creating page content, test the chat with the content by sending a `POST` HTTP request to the `/v1/chat` endpoint.
