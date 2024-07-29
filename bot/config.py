from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    BOT_TOKEN: str
    SECRET_KEY: str
    DB_URL: str
    OPENROUTESERVICE_API_KEY: str


config = Config()  # type: ignore
