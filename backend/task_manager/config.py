from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_PASS: str
    DB_USER: str
    DB_SCHEMA: str

    DB_HOST_TEST: str
    DB_PORT_TEST: int
    DB_NAME_TEST: str
    DB_PASS_TEST: str
    DB_USER_TEST: str

    SECRET: str

    @property
    def database_url(self):
        DATABESE_URL = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return DATABESE_URL

    @property
    def database_url_test(self):
        DATABESE_URL = f"postgresql+asyncpg://{self.DB_USER_TEST}:{self.DB_PASS_TEST}@{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}"
        return DATABESE_URL

    model_config = SettingsConfigDict(env_file=None)


settings = Settings()
