from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Telegram Bot
    BOT_TOKEN: str
    # PostgreSQL Database
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int = 6379  # Redis по умолчанию работает на 6379

    # FastAPI Server
    WEBAPP_HOST: str = "0.0.0.0"  # Запуск на всех интерфейсах
    WEBAPP_PORT: int = 8000  # Порт FastAPI

    # NGROK / External Base URL
    BASE_URL: str  # Твой ngrok-адрес для вебхуков

    # Логирование
    LOG_LEVEL: str = "info"

    NGINX_HOST:str= 'http://nginx'

    class Config:
        env_file = "../env/main.env"  # Явно указываем .env


    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        # a = f"postgresql+asyncpg://postgres:postgres@postgres_main:5432/b_base"

settings = Settings(
    BOT_TOKEN='<BOT_TOKEN>',
    DB_HOST='postgres1503',
    DB_PORT=5432,
    DB_NAME='b_base',
    DB_USER='postgres',
    DB_PASS='postgres',
    BASE_URL='https://fourpizzabot.com',
    REDIS_HOST='redis1503',
    REDIS_PORT=6379,
    WEBAPP_HOST='0.0.0.0',
    WEBAPP_PORT=8000,
    LOG_LEVEL="info",
    NGINX_HOST='http://nginx'
)


