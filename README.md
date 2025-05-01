## Requirements
- Docker engine
- Code IDE ( I m using Cursor)
- psql (command line to interact with Postgress). We will use RisingWave database which is based on Postgress

## Tools for Kubernetics
- kind: To spin up local kubernetics cluster
- Kubectl : To interact with Kubernetics cluster
- k9s: command utility to interact with kubernetics cluster
- helm: package manager for kubernetics
- direnv: tool to manage your env variables. We will mostly use it to load right KUBECONFIG environment variable so that kubectl knows whether we want to talk to local kubernetics cluster or prod kubernetics cluster

## To start local Kubernetics cluster, refer https://github.com/Paulescu/kubernetes-for-ml-engineers
- kind create cluster --config kind.yaml --name cluster-123
- kubectl config use-context kind-cluster-123
- kubectl get nodes -A


