## Goals

- How to deploy Kafka in dev k8s cluster
    - create a namespace : > kafka create namespace kafka
    - install kafka from strimzi : > kubectl create -f https://strimzi.io/latest/workspace=kafka -n kafka
    - kubectl apply -f manifests/kafka-e11b.yaml
- Deploy Kafka UI in dev k8 cluster for visibility into Kafka   
    - use deployments/dev/kind/install_kafka_ui.sh
    - expose kafka-ui service to host using port forwarding
        > kubectl -n kafka port-forward svc/kafka-ui 8192:8080
- In order to process real time data before feeding it into kafka, we need some library, we have Apache Spark (written in Java which is hard to debug), we can use something written in python like Quixstreams, Bytewax. Here we will install quixstreams
    > uv add quixstreams

- Now we should push some dummy data to kafka which is up and running inside k8s, but we need to talk to kafka broker in order to push data to kafka via quixstream. The deployments/dev/kind/kind-with-portmapping.yaml expose kafka broker at localhost:31234
    ```
    # Expose Kafka broker to localhost:31234
        - containerPort: 31234
        hostPort: 31234
        listenAddress: "127.0.0.1"
        protocol: TCP
    ```
    Quick Tip to check kafka borker connectivity from localhost
    ```
    nc -vvv localhost 31234
    ```