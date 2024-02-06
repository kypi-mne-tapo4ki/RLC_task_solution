from functools import lru_cache

import yaml


class Settings:
    jwt_secret_key: str
    database_url: str
    jwt_algorithm = "HS256"
    token_expire_minutes = 60

    def __init__(self, **kwargs):
        for setting_key, setting_value in kwargs.items():
            setattr(self, setting_key, setting_value)

    @classmethod
    def load(cls):
        with open("config.yaml") as config:
            config_data = yaml.safe_load(config)
            return cls(**config_data)


settings = lru_cache(Settings.load)()
