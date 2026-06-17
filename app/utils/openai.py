from openai import OpenAI

from app.core.settings import settings


def get_openai_client() -> OpenAI:
    if settings.openrouter_api_key is None:
        raise RuntimeError("OPENROUTER_API_KEY is required")

    return OpenAI(
        api_key=settings.openrouter_api_key,
        base_url="https://openrouter.ai/api/v1",
    )
