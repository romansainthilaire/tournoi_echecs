from pathlib import Path
from datetime import datetime
from typing import List

from tinydb import TinyDB

from models.match import Match


db = TinyDB(Path(__file__).parent.parent / "db.json", indent=4)
rounds_table = db.table("rounds")


class Round:

    DATE_FORMAT: str = "%d/%m/%Y %H:%M:%S"

    def __init__(self, name: str):
        self.id: int = -1
        self.name: str = name
        self.matches: List[Match] = []
        self.start: datetime = datetime.now()
        self.end: datetime = datetime.max
        self.in_progress: bool = True

    def __str__(self):
        start = self.start.strftime(Round.DATE_FORMAT)
        end = self.end.strftime(Round.DATE_FORMAT)
        if self.in_progress:
            return (
                f"\nID {self.id} \t{self.name}"
                f"\n\tDébut : {start}"
                "\n\tFin : (en cours)"
            )
        else:
            return (
                f"\nID {self.id}\t{self.name}"
                f"\n\tDébut : {start}"
                f"\n\tFin : {end}"
            )

    @property
    def serialized(self):
        return {
            "id": self.id,
            "name": self.name,
            "matches": [match.serialized for match in self.matches],
            "start": self.start.strftime(Round.DATE_FORMAT),
            "end": self.end.strftime(Round.DATE_FORMAT),
            "in_progress": self.in_progress
        }

    def save(self):
        if self.id < 0:
            self.id = rounds_table.insert(self.serialized)
            rounds_table.update({"id": self.id}, doc_ids=[self.id])
        else:
            rounds_table.update(self.serialized, doc_ids=[self.id])

    def add_match(self, match: Match):
        self.matches.append(match)
        self.save()

    def finish(self):
        self.end = datetime.now()
        self.in_progress = False
        self.save()
