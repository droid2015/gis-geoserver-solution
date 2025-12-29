from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    POSTGRES_HOST: str = "postgres-postgis"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "gisdb"
    POSTGRES_USER: str = "gisuser"
    POSTGRES_PASSWORD: str = "changeme_gispassword"
    
    # GeoServer
    GEOSERVER_URL: str = "http://geoserver:8080/geoserver"
    GEOSERVER_ADMIN_USER: str = "admin"
    GEOSERVER_ADMIN_PASSWORD: str = "geoserver"
    
    # Application
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "your-secret-key-change-this"
    CORS_ORIGINS: str = "http://localhost:3000"
    
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
