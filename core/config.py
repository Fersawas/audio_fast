from pydantic_settings import BaseSettings
from pydantic import SecretStr
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAYS: str
    REFRESH_TOKEN_EXPIRE_DAYS: str


settings = Settings()


def get_auth_data():
    return {
        "secret_key": settings.SECRET_KEY,
        "algorithm": settings.ALGORITHM,
        "access_token_expire": settings.ACCESS_TOKEN_EXPIRE_DAYS,
        "refresh_token_expire": settings.REFRESH_TOKEN_EXPIRE_DAYS,
    }
