from pathlib import Path

from tinydb import TinyDB

from models.player import Player


db = TinyDB(Path(__file__).parent.parent / "db.json", indent=4)
matches_table = db.table("matches")


class Match(tuple):

    def __new__(
        cls,
        player_1: Player,
        score_1: int,
        player_2: Player,
        score_2: int
    ):
        return tuple.__new__(Match, ([player_1, score_1], [player_2, score_2]))

    def __str__(self):
        return (
            f"{self[0][0].first_name} {self[0][0].last_name} : {self[0][1]}"
            + "\n"
            f"{self[1][0].first_name} {self[1][0].last_name} : {self[1][1]}"
            )

    @property
    def serialized(self):
        return {
            "player_1": self[0][0].serialized,
            "score_1": self[0][1],
            "player_2": self[1][0].serialized,
            "score_2": self[1][1],
        }

    def save(self):
        self.id = matches_table.insert(self.serialized)
