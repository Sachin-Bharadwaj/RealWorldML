## Session 2

### Goals

    - [] Build a docker image for our trade service (refer Makefile)
    - [] Deploy this image to our k8s dev cluster
        - [] Push image to the local registry inside k8s (by default there is registry service which kind spins up inside local k8s cluster)
            - Check the cluster name: >kind get clusters
            - push the image to our local dev cluster: >kind load docker-image <image_name> --name <cluster_name>
            - to deploy, there is a trades.yaml file inside deployments/dev/trades/trades.yaml
            you run >kubectl apply -f <filename.yaml>
        - [] we need to write deployment.yaml file for our dev k8s cluster
        - [] we need to trigger the deployment (manually) `kubectl apply -f ...`
    - [] configs for trade service via Pydantic BaseSettings
    - [] Use precommits for formatting and linting automatically
        - [] install `ruff` and `precommit`
        - [] add/install precommit hooks
            - [] create and copy ruff precommit.yaml from ruff github repo as .pre-commit-config.yaml
            - [] Run following to install pre-commit hooks >pre-commit install
