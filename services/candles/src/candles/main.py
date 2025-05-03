from quixstreams import Application
from loguru import logger
from datetime import timedelta


def init_candle(trade: dict) -> dict:
    return {
        "open": trade["price"],
        "high": trade["price"],
        "low": trade["price"],
        "close": trade["price"],
        "volume": trade["quantity"],
        # "timestamp": trade["timestamp"],
        "symbol": trade["product_id"],
    }


def update_candle(candle: dict, trade: dict) -> dict:
    # update the candle with the new trade
    candle["high"] = max(candle["high"], trade["price"])
    candle["low"] = min(candle["low"], trade["price"])
    candle["close"] = trade["price"]
    candle["volume"] += trade["quantity"]
    return candle


def main(
    kafka_broker_address: str,
    kafka_input_topic_name: str,
    kafka_output_topic_name: str,
    candles_seconds: int,
    emit_intermediate_candles: bool = True,
):
    app = Application(broker_address=kafka_broker_address, consumer_group="candles")

    # Define a topic "my_topic" with JSON serialization
    input_topic = app.topic(name=kafka_input_topic_name, value_serializer="json")
    output_topic = app.topic(name=kafka_output_topic_name, value_serializer="json")

    # STEP1: Ingest the trades into a streaming DataFrame
    # create a streaming DataFrame from the input topic
    sdf = app.dataframe(topic=input_topic)

    # STEP2: Transform the trades into candles
    # At the moment I am just printing the trades (TODO)
    sdf = (
        # create a tumbling count window
        sdf.tumbling_window(timedelta(seconds=candles_seconds))
        # create a reduce aggreation with a reducer and initialization function
        .reduce(reducer=update_candle, initializer=init_candle)
    )

    if emit_intermediate_candles:
        # emit the intermediate candles to make system more responsive
        sdf = sdf.current()
    else:
        sdf = sdf.final()

    # sdf.update(lambda message: logger.info(f"Received message: {message}"))

    # Extract open, high, low, close, volume, timestamp_ms, pair from the dataframe
    sdf["open"] = sdf["value"]["open"]
    sdf["high"] = sdf["value"]["high"]
    sdf["low"] = sdf["value"]["low"]
    sdf["close"] = sdf["value"]["close"]
    sdf["volume"] = sdf["value"]["volume"]
    # sdf['timestamp_ms'] = sdf['value']['timestamp_ms']
    sdf["symbol"] = sdf["value"]["symbol"]

    # Extract window start and end timestamps
    sdf["window_start_ms"] = sdf["start"]
    sdf["window_end_ms"] = sdf["end"]

    # keep only the relevant columns
    sdf = sdf[
        [
            "symbol",
            # 'timestamp_ms',
            "open",
            "high",
            "low",
            "close",
            "volume",
            "window_start_ms",
            "window_end_ms",
        ]
    ]

    sdf["candle_seconds"] = candles_seconds

    # logging on the console
    sdf = sdf.update(lambda value: logger.debug(f"Candle: {value}"))

    # STEP3: Write the candles to the output topic
    sdf.to_topic(topic=output_topic)

    # STEP4: Start the application
    app.run()


if __name__ == "__main__":
    main(
        kafka_broker_address="localhost:31234",
        kafka_input_topic_name="kraken_trades",
        kafka_output_topic_name="kraken_candles",
        candles_seconds=10,
    )
