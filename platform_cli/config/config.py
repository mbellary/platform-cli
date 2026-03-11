from pydantic import BaseModel


class CLIConfig(BaseModel):
    api_url: str
    api_key: str | None = None
