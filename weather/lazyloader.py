import json


class LazyLoader:
    def __init__(self, filename: str):
        self.filename = filename

    @property
    def content(self) -> dict:
        if hasattr(self, '_content'):
            return self._content
        with open(self.filename, "r", encoding="utf8") as file:
            self._content = json.load(file)
        return self._content
