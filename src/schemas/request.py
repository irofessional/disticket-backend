from typing import Optional, List

from pydantic import BaseModel, Field

class Request(BaseModel):
    url: str
    site: str