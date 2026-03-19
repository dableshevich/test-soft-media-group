from pydantic import PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Project settings"""

    # APPLICATION SETTINGS
    DEBUG: bool = False
    APP_TITLE: str = "Test Assignment"
    APP_DESCRIPTION: str = 'Test assignment for "Soft Media Group"'
    API_PREFIX: str = "/api/v1"

    # POSTGRESQL AUTH DATA
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: SecretStr = SecretStr("postgres")  # noqa: F821
    POSTGRES_DB: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    # REDIS SETTINGS
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: str = "0"
    REDIS_TTL: int = 15

    @property
    def DATABASE_URL(self) -> str:
        dsn = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.POSTGRES_DB,
        )
        return str(dsn)

    @property
    def REDIS_URL(self) -> str:
        dsn = RedisDsn.build(
            scheme="redis",
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            path=self.REDIS_DB,
        )
        return str(dsn)


settings = Settings()
