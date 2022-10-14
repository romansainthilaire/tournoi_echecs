from pathlib import Path

from typing import Optional

from tinydb import TinyDB

from models.player import Player


db = TinyDB(Path(__file__).parent.parent / "db.json", indent=4)
matches_table = db.table("matches")


class Match():
    """Represents a match between two chess players."""

    def __init__(self, player_1: Player, player_2: Player):
        """Inits a match.

        Arguments:
            player_1 -- first player
            player_2 -- second player
        """
        self.id: Optional[int] = None
        self.player_1: Player = player_1
        self.player_2: Player = player_2
        self.score_1: Optional[float] = None
        self.score_2: Optional[float] = None

    def __str__(self):
        """String representation of a match."""
        score_1 = "" if self.score_1 is None else f" : {self.score_1}"
        score_2 = "" if self.score_2 is None else f" : {self.score_2}"
        return (
            f"\nID {self.id}"
            f"\t{self.player_1.name}{score_1}" + "\n"
            f"\t{self.player_2.name}{score_2}"
        )

    @property
    def serialized(self):
        """Turns a match object into a dictionary.

        Returns:
            A dictionary of the match attributes.
        """
        return {
            "id": self.id,
            "player_1": self.player_1.serialized,
            "player_2": self.player_2.serialized,
            "score_1": self.score_1,
            "score_2": self.score_2,
        }

    def save(self):
        """Inserts or updates a match into a TinyDB database."""
        if self.id is None:
            self.id = matches_table.insert(self.serialized)
            matches_table.update({"id": self.id}, doc_ids=[self.id])
        else:
            matches_table.update(self.serialized, doc_ids=[self.id])
        self.player_1.save()
        self.player_2.save()
