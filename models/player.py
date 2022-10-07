from pathlib import Path
from datetime import date

from tinydb import TinyDB


db = TinyDB(Path(__file__).parent.parent / "db.json", indent=4)
players_table = db.table("players")


class Player:

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birth_day: int,
        birth_month: int,
        birth_year: int,
        sex: str,
        ranking: int = 0
    ):
        self.first_name = first_name.title()
        self.last_name = last_name.upper()
        self.date_of_birth = date(birth_year, birth_month, birth_day)
        self.sex = sex
        self.ranking = ranking

    def __str__(self):
        return (
            f"{self.first_name} {self.last_name} ({self.sex})" + "\n"
            f"Né le {self.date_of_birth.strftime('%d/%m/%Y')}" + "\n"
            f"Classement : {self.ranking}"
            )

    @property
    def serialized(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth.strftime("%d/%m/%Y"),
            "sex": self.sex,
            "ranking": self.ranking
        }

    def save(self):
        self.id = players_table.insert(self.serialized)

    def set_ranking(self, ranking: int):
        self.ranking = ranking
