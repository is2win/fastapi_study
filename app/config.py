from pydantic_settings import BaseSettings
from pydantic import root_validator, model_validator, validator



class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    USER_KEY: str
    USER_ALGORITM: str
    DATABASE_URL: str = ''

    @validator("DATABASE_URL", pre=True, always=True)
    def assemble_database_url(cls, v, values):
        if all(field in values for field in ('DB_USER', 'DB_PASS', 'DB_HOST', 'DB_PORT', 'DB_NAME')):
            return f"postgresql+asyncpg://{values['DB_USER']}:{values['DB_PASS']}@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"
        return v

    class Config:
        env_file = ".env"
        extra = 'forbid'


settings = Settings()
# print(settings.DATABASE_URL)