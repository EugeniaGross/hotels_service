from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    model_config = SettingsConfigDict(env_file=".env")
    
    @property
    def DB_URL(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        
        
settings = Settings()