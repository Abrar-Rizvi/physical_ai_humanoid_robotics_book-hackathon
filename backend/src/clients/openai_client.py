from openai import OpenAI
from ..config import settings


def create_openai_client() -> OpenAI:
    """
    Create and configure OpenAI client with API key from settings
    """
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    client = OpenAI(api_key=settings.openai_api_key)
    return client


# Global client instance
openai_client = create_openai_client()