import os
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

EnvironmentType = Literal["prod", "local", "dev", "test"]

g_app_mode = os.getenv('DISCORD_APP_MODE', 'prod')

if g_app_mode is None:
    g_app_mode = 'prod'


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=f".env.{g_app_mode}")
    APP_MODE: str = g_app_mode

    # discord bot
    BOT_KEY: str
    # open ai
    OPEN_AI_KEY: str

    ## db section
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_ADDRESS: str = '127.0.0.1'
    DATABASE_NAME: str
    DATABASE_AUTO_COMMIT: bool = False
    DATABASE_AUTO_FLUSH: bool = False

    @staticmethod
    def load_env(app_mode: EnvironmentType = g_app_mode) -> "EnvSettings":
        target_env_file = f".env.{app_mode}"

        # 내부 클래스 선언해서 원하는 환경 로드 하도록.
        class ConfiguredEnvSettings(EnvSettings):
            model_config = SettingsConfigDict(env_file=target_env_file)

        return ConfiguredEnvSettings()

    def is_prod(self) -> bool:
        return self.APP_MODE == 'prod'
