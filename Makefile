.PHONY: install
install:
	pip install -r requirements-dev.txt && pre-commit install;

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
	docker-compose up --build;

.PHONY: docker-up-detached
docker-up-detached: ## Bring up environment in Docker detached mode
	docker-compose up --build -d;

.PHONY: docker-db-upgrade
docker-db-upgrade:
	docker-compose exec fastapi_service alembic upgrade head;

.PHONY: docker-run
docker-run: docker-up-detached docker-db-upgrade
