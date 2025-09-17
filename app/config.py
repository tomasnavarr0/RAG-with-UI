from openai import AsyncOpenAI
from literalai import LiteralClient
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Clase para cargar configuraciones desde variables de entorno utilizando Pydantic.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    OPENAI_API_KEY: str
    LITERAL_API_KEY: str
    ASSISTANT_ID: str
    VECTOR_DB_ID: str

    OLLAMA_HOST: str
    OLLAMA_MODEL: str

    PDF_FOLDER: str = "app/data"

    @property
    def literal_client(self) -> LiteralClient:
        return LiteralClient(api_key=self.LITERAL_API_KEY)

    @property
    def async_openai_client(self) -> AsyncOpenAI:
        self.literal_client.instrument_openai()
        return AsyncOpenAI(api_key=self.OPENAI_API_KEY, http_client=None)


Settings = Settings()  # type: ignore
