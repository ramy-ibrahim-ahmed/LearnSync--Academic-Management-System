from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRE_USERNAME: str
    POSTGRE_PASSWORD: str

    class Config:
        env_file = r".env"


def get_settings():
    return Settings()
