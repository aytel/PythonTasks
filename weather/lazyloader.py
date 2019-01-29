import json

from utils import levenstein


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

    def get_closest(self, element):
        content = self.content

        cur, min_dist = None, float('inf')
        for cand_name in map(lambda x: x["name"], content):
            val = levenstein(element.lower(), cand_name.lower())
            if val < min_dist:
                cur, min_dist = cand_name, val

        return cur

