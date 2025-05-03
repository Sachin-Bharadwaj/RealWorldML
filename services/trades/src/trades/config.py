from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="services/trades/src/trades/settings.env"
    )
    product_ids: List[str] = ["BTC/USD", "ETH/USD"]
    kafka_broker_address: str
    kafka_topic: str


settings = Settings()
