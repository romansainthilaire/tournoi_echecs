from pathlib import Path
from datetime import datetime
from typing import List

from tinydb import TinyDB

from models.match import Match


db = TinyDB(Path(__file__).parent.parent / "db.json", indent=4)
rounds_table = db.table("rounds")


class Round:

    def __init__(self, name: str, matches: List[Match]):
        self.name = name
        self.matches = matches
        self.start = datetime.now()
        self.end = datetime.max

    def __str__(self):
        return (
            f"{self.name}" + "\n"
            f"Début : {self.start.strftime('%d/%m/%Y %H:%M:%S')}" + "\n"
            f"Fin : {self.end.strftime('%d/%m/%Y %H:%M:%S')}"
            )

    @property
    def serialized(self):
        return {
            "name": self.name,
            "matches": [match.serialized for match in self.matches],
            "start": self.start.strftime("%d/%m/%Y %H:%M:%S"),
            "end": self.end.strftime("%d/%m/%Y %H:%M:%S"),
        }

    def save(self):
        self.id = rounds_table.insert(self.serialized)

    def finish(self):
        self.end = datetime.now()
        updated_data = {"end": self.end.strftime("%d/%m/%Y %H:%M:%S")}
        rounds_table.update(updated_data, doc_ids=[self.id])
