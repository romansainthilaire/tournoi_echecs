from pathlib import Path

from tinydb import TinyDB, where


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
        self.id = -1
        self.first_name = first_name.title()
        self.last_name = last_name.upper()
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.ranking = ranking
        self.points = float(0)
        self.opponent_ids = []
        self.name = self.first_name + " " + self.last_name

    def __str__(self):
        return (
            f"\nID {self.id}" +
            f"\t{self.name} ({self.sex})" + "\n"
            f"\tNé le {self.date_of_birth}" + "\n"
            f"\tClassement : {self.ranking}"
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
            "opponent_ids": self.opponent_ids
        }

    def save(self):
        if self.id < 0:
            self.id = players_table.insert(self.serialized)
            players_table.update({"id": self.id}, doc_ids=[self.id])
        else:
            players_table.update(
                self.serialized,
                where("id") == self.id  # type: ignore
            )

    def set_ranking(self, ranking: int):
        self.ranking = ranking
        self.save()
