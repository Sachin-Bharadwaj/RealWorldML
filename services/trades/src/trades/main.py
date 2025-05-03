# Create an Application instance with Kafka configs
from quixstreams import Application
from kraken_api import KrakenAPI, Trade
from typing import List
from loguru import logger
from config import settings


def main(kafka_broker_address: str, kafka_topic_name: str, kraken_api: KrakenAPI):
    app = Application(broker_address=kafka_broker_address, consumer_group="example")

    # Define a topic "my_topic" with JSON serialization
    topic = app.topic(name=kafka_topic_name, value_serializer="json")

    # Create a Producer instance
    with app.get_producer() as producer:
        while True:
            # Fetch the data from external source/API
            ## in this case we have fake data
            # event = {"id": "1", "text": "Lorem ipsum dolor sit amet"}

            events: List[Trade] = kraken_api.get_trades()

            for event in events:
                # Serialize an event using3 the defined Topic
                message = topic.serialize(  # key=event["id"],
                    value=event.to_dict()
                )

                # Produce a message into the Kafka topic
                producer.produce(
                    topic=topic.name,
                    value=message.value,
                    # key=message.key
                )

                logger.info(f"Produced message: {message.value} to topic: {topic.name}")


if __name__ == "__main__":
    kafka_broker_address = settings.kafka_broker_address
    kafka_topic_name = settings.kafka_topic
    api = KrakenAPI(product_ids=settings.product_ids)
    main(kafka_broker_address, kafka_topic_name, api)
