from pathlib import Path
from typing import List, Optional

from tinydb import TinyDB


db = TinyDB(Path(__file__).parent.parent / "db.json", indent=4)
players_table = db.table("players")


class Player:

    def __init__(
        self,
        first_name: str,
        last_name: str,
        date_of_birth: str,
        sex: str,
        ranking: int
    ):
        self.id: int = -1
        self.first_name: str = first_name.title()
        self.last_name: str = last_name.upper()
        self.date_of_birth: str = date_of_birth
        self.sex: str = sex
        self.ranking: int = ranking
        self.points: float = 0
        self.opponent_ids: List[int] = []
        self.tournament_id: Optional[int] = None
        self.name: str = self.first_name + " " + self.last_name

    def __str__(self):
        info = ""
        if self.tournament_id is None:
            info = "\n\tDisponible"
        else:
            info = f"\n\tID Tournoi : {self.tournament_id}"
        return (
            f"\nID {self.id}"
            f"\t{self.name} ({self.sex})"
            f"\n\tNé le {self.date_of_birth}"
            f"\n\tClassement Elo : {self.ranking}"
            + info
        )

    @property
    def serialized(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "sex": self.sex,
            "ranking": self.ranking,
            "points": self.points,
            "opponent_ids": self.opponent_ids,
            "tournament_id": self.tournament_id
        }

    def save(self):
        if self.id < 0:
            self.id = players_table.insert(self.serialized)
            players_table.update({"id": self.id}, doc_ids=[self.id])
        else:
            players_table.update(self.serialized, doc_ids=[self.id])

    def set_ranking(self, ranking: int):
        self.ranking = ranking
        self.save()

    def reset(self):
        self.points = 0
        self.opponent_ids = []
        self.tournament_id = None
        self.save()
