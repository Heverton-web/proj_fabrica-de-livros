from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Máquina de Vendas"
    DEBUG: bool = False
    DATABASE_URL: str = "sqlite:///./data/vendas.db"
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "contato@fabricadelivros.com.br"
    WEBHOOK_SECRET: str = "change-me"
    SCORING_PESO_ABERTURA: float = 15.0
    SCORING_PESO_CLIQUE: float = 25.0
    SCORING_PESO_RESPOSTA: float = 30.0
    SCORING_PESO_VISITA: float = 20.0
    SCORING_PESO_download: float = 10.0

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
