from typing import List
from pydantic import BaseModel
from websocket import create_connection
import json
from loguru import logger

class Trade(BaseModel):
    product_id: str
    price: float
    quantity: float
    timestamp: str

    def to_dict(self):
        """
        converts self to a dict object
        """
        return self.model_dump()

class KrakenAPI:
    URL = "wss://ws.kraken.com/v2"
    def __init__(self, 
                 product_ids: List[str]):
        self.product_ids = product_ids

        # connect to the websocket connection
        self._ws = create_connection(self.URL)

        # subscribe to the product ids
        self._subscribe()
        
    def get_trades(self) -> List[Trade]:
        # get the data from the websocket
        data = self._ws.recv() # this data is a json string
 
        if 'heartbeat' in data:
            logger.info("Heartbeat received")
            return []
        
        try:
            # parse the data
            data = json.loads(data)
        except json.JSONDecodeError:
            logger.error(f"Error parsing data: {data}")
            return []

        try:
            # get the trades
            trades_data = data["data"]
        except KeyError as e:
            logger.error(f"Error getting `data` key from websocket data: {e}")
            return []
        
        trades = [Trade(
            product_id=trade["symbol"],
            price=trade["price"],
            quantity=trade["qty"],
            timestamp=trade["timestamp"]
        ) for trade in trades_data]
        


        return trades

    def _subscribe(self):
        self._ws.send(json.dumps({
            "method": "subscribe",
            "params": {
                "channel": "trade",
                "symbol": self.product_ids,
                "snapshot": False
            }
        }))

        # ignore first couple of messages from Kraken for every subscribed product since it is handoff related message
        for _ in range(len(self.product_ids)):
            self._ws.recv()
            self._ws.recv()

