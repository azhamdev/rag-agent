from mistralai.client import Mistral

from app.core.settings import settings

def get_mistral_client() -> Mistral:
    if settings.mistralai_api_key is None:
        raise RuntimeError("MISTRAL_API_KEY is required")

    return Mistral(api_key=settings.mistralai_api_key)

