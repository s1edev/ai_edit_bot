from dataclasses import dataclass
from environs import Env


@dataclass
class ChannalSet:
    id: int
    url: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    polza_api: str
    imgbb_api: str


@dataclass
class Config:
    bot: TgBot
    channal: ChannalSet


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)
    return Config(
        bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS'))),
            polza_api=env('POLZA_API'),
            imgbb_api=env('IMGBB_API')
        ),
        channal=ChannalSet(
            id=env.int('CHANNEL_ID'),
            url=env('CHANNEL_URL')
        ),
    )
