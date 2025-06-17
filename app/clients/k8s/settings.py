from typing import Optional

from pydantic_settings import BaseSettings


class K8SSettings(BaseSettings):
    incluster: bool
    context: Optional[str]
    timeout_seconds: int
