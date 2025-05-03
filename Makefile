# run the trade service as standalone python script (for development, not Dockerized)
dev:
	# uv run services/trades/src/trades/main.py
	uv run services/${service}/src/${service}/main.py

build:
	# DOCKER_BUILDKIT=1 docker buildx build -t kraken-trades:dev -f docker/trades.Dockerfile .
	DOCKER_BUILDKIT=1 docker buildx build -t ${image_name} -f docker/${service}.Dockerfile .

push:
	kind load docker-image ${image_name} --name rwml-34fa

deploy: build push
	kubectl get -f deployments/dev/trades/trades.yaml >/dev/null 2>&1 && kubectl delete -f deployments/dev/trades/trades.yaml || true
	kubectl apply -f deployments/dev/trades/trades.yaml

lint:
	ruff check . --fix

format:
	ruff format .




