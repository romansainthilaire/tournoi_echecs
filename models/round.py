from pathlib import Path
from datetime import datetime
from typing import List

from tinydb import TinyDB, where

from models.match import Match


db = TinyDB(Path(__file__).parent.parent / "db.json", indent=4)
rounds_table = db.table("rounds")


class Round:

    def __init__(
        self,
        name: str,
        matches: List[Match] = [],
        start: datetime = datetime.now(),
        end: datetime = datetime.max,
        in_progress: bool = True
    ):
        self.id = -1
        self.name = name
        self.matches = matches
        self.start = start
        self.end = end
        self.in_progress = in_progress

    def __str__(self):
        start = self.start.strftime("%d/%m/%Y %H:%M:%S")
        end = self.end.strftime("%d/%m/%Y %H:%M:%S")
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
            "start": self.start.strftime("%d/%m/%Y %H:%M:%S"),
            "end": self.end.strftime("%d/%m/%Y %H:%M:%S"),
            "in_progress": self.in_progress
        }

    def save(self):
        if self.id < 0:
            self.id = rounds_table.insert(self.serialized)
            rounds_table.update({"id": self.id}, doc_ids=[self.id])
        else:
            rounds_table.update(
                self.serialized,
                where("id") == self.id  # type: ignore
            )

    def add_match(self, match: Match):
        self.matches.append(match)
        self.save()

    def finish(self):
        self.end = datetime.now()
        self.in_progress = False
        self.save()
