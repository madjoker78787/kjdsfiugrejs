
class Settings:
    DB_NAME: str = "Telegram"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    TABLE_TELEGRAM: str = "data"

    PROXY: str = "http://dfxhfhaw-rotate:rdhoxlgxoqub@p.webshare.io:80/"
    WORKERS: int = 5


settings = Settings()
