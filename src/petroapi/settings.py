from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    admin_email: str
    admin_password: str

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int

    dbhost: str
    dbname: str
    dbuser: str
    dbpassword: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.dbuser}:{self.dbpassword}@{self.dbhost}/{self.dbname}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
