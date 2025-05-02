
# Variables
DOCKER_COMPOSE_FILE := docker-compose.yml
COMPOSE=docker compose -f $(DOCKER_COMPOSE_FILE)

.PHONY: install
install:
	uv sync && pre-commit install;

.PHONY: db-migrate
db-migrate:
	alembic revision --autogenerate;

.PHONY: db-upgrade
db-upgrade:
	alembic upgrade head;

.PHONY: run
run:
	python run.py;

.PHONY: test
test:
	pytest -vv;

.PHONY: docker-up
docker-up:
	$(COMPOSE) up --build;

.PHONY: docker-up-detached
docker-up-detached: ## Bring up environment in Docker detached mode
	$(COMPOSE) up --build -d;

.PHONY: docker-db-upgrade
docker-db-upgrade:
	$(COMPOSE) exec fastapi alembic upgrade head;

.PHONY: docker-run
docker-run: docker-up-detached docker-db-upgrade
