import configparser
from dataclasses import dataclass


@dataclass(frozen=True)
class Telegram:
    token: str


@dataclass(frozen=True)
class Redis:
    host: str
    port: int = 6379
    user: str | None = None
    password: str | None = None
    db_name: str = 10


@dataclass(frozen=True)
class Config:

    telegram: Telegram
    redis: Redis


def read_config(config_path: str) -> Config:
    """Config factory."""
    config = configparser.ConfigParser()
    config.read(config_path)

    db = config['redis']
    tg = config['telegram']

    return Config(
        Telegram(tg.get('TOKEN')),
        Redis(db.get('HOST'))
    )
