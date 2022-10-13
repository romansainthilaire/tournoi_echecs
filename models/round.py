from pathlib import Path
from datetime import datetime
from typing import List, Optional

from tinydb import TinyDB

from models.match import Match


db = TinyDB(Path(__file__).parent.parent / "db.json", indent=4)
rounds_table = db.table("rounds")


class Round:
    """Represents a round of a chess tournament."""

    DATE_FORMAT: str = "%d/%m/%Y %H:%M:%S"

    def __init__(self, name: str):
        """Inits a round.

        Arguments:
            name -- name of the round
        """
        self.id: Optional[int] = None
        self.name: str = name
        self.matches: List[Match] = []
        self.start: datetime = datetime.now()
        self.end: datetime = datetime.max
        self.in_progress: bool = True

    def __str__(self):
        """String representation of a match."""
        start = self.start.strftime(Round.DATE_FORMAT)
        end = self.end.strftime(Round.DATE_FORMAT)
        end_or_in_progress = end if not self.in_progress else "en cours"
        return (
            f"\nID {self.id}\t{self.name}"
            f"\n\tDébut : {start}"
            f"\n\tFin : {end_or_in_progress}"
        )

    @property
    def serialized(self):
        """Turns a round object into a dictionary.

        Returns:
            A dictionary of the round attributes.
        """
        return {
            "id": self.id,
            "name": self.name,
            "matches": [match.serialized for match in self.matches],
            "start": self.start.strftime(Round.DATE_FORMAT),
            "end": self.end.strftime(Round.DATE_FORMAT),
            "in_progress": self.in_progress
        }

    def save(self):
        """Saves or updates a round into a TinyDB database."""
        if self.id is None:
            self.id = rounds_table.insert(self.serialized)
            rounds_table.update({"id": self.id}, doc_ids=[self.id])
        else:
            rounds_table.update(self.serialized, doc_ids=[self.id])
            for match in self.matches:
                match.save()

    def add_match(self, match: Match):
        """Adds a match to the round.

        Arguments:
            match -- match object
        """
        self.matches.append(match)
        self.save()

    def finish(self):
        """Ends the round."""
        self.end = datetime.now()
        self.in_progress = False
        self.save()
