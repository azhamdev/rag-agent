from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Rag Engine"
    app_version: str = "0.1.0"
    app_description: str = "Rag Engine"

    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str | None = None
    celery_result_backend: str | None = None

    cors_allow_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    database_url: str = "sqlite:///./app.db"
    database_echo: bool = False

    document_upload_dir: str = "uploads"

    mistralai_api_key: str | None = None
    mistral_ocr_model: str = "mistral-ocr-2512"

    openai_api_key: str | None = None
    openai_keypoint_model: str = "gpt-4.1-mini"

    openrouter_api_key: str | None = None

    chroma_db_path: str = "chroma_db"
    chroma_collection_name: str = "document_pages"

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def celery_broker(self) -> str:
        return self.celery_broker_url or self.redis_url

    @property
    def celery_backend(self) -> str:
        return self.celery_result_backend or self.redis_url


settings = Settings()
