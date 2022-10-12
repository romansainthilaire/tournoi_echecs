from pathlib import Path

from typing import Optional

from tinydb import TinyDB

from models.player import Player


db = TinyDB(Path(__file__).parent.parent / "db.json", indent=4)
matches_table = db.table("matches")


class Match():

    def __init__(self, player_1: Player, player_2: Player):
        self.id: int = -1
        self.player_1: Player = player_1
        self.player_2: Player = player_2
        self.score_1: Optional[float] = None
        self.score_2: Optional[float] = None

    def __str__(self):
        score_1 = "" if self.score_1 is None else f" : {self.score_1}"
        score_2 = "" if self.score_2 is None else f" : {self.score_2}"
        return (
            f"\nID {self.id}"
            f"\t{self.player_1.name}{score_1}" + "\n"
            f"\t{self.player_2.name}{score_2}"
        )

    @property
    def serialized(self):
        return {
            "id": self.id,
            "player_1": self.player_1.serialized,
            "player_2": self.player_2.serialized,
            "score_1": self.score_1,
            "score_2": self.score_2,
        }

    def save(self):
        if self.id < 0:
            self.id = matches_table.insert(self.serialized)
            matches_table.update({"id": self.id}, doc_ids=[self.id])
        else:
            matches_table.update(self.serialized, doc_ids=[self.id])
