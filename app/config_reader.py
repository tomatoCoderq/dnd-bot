import configparser
from dataclasses import dataclass


@dataclass
class Bot:
    token: str


@dataclass
class Config:
    tg_bot: Bot


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    bot = config["bot"]

    return Config(
        tg_bot=Bot(
            token=bot["token"],
        )
    )
