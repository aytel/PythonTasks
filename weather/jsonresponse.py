from dataclasses import dataclass


@dataclass
class JSONResponse:
    code: int or None
    content: str or None
    error: Exception or None
    new_city: str or None = None
