# run the trade service as standalone python script (for development, not Dockerized)
dev:
	uv run services/trades/src/trades/main.py

build:
	DOCKER_BUILDKIT=1 docker buildx build -t kraken-trades:dev -f docker/trades.Dockerfile .

push:
	kind load docker-image kraken-trades:dev --name rwml-34fa

deploy: build push
	kubectl delete -f deployments/dev/trades/trades.yaml
	kubectl apply -f deployments/dev/trades/trades.yaml

lint:
	ruff check . --fix

format:
	ruff format .




