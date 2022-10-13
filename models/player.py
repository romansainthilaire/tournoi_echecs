from pathlib import Path
from typing import List, Optional

from tinydb import TinyDB


db = TinyDB(Path(__file__).parent.parent / "db.json", indent=4)
players_table = db.table("players")


class Player:
    """Represents a chess player."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        date_of_birth: str,
        sex: str,
        ranking: int
    ):
        """Inits a player.

        Arguments:
            first_name -- first name of the player
            last_name -- last name of the player
            date_of_birth -- date of birth of the player (format : DD/MM/YYYY)
            sex -- sex of the player ("M" or "F")
            ranking -- Elo ranking of the player (> 0)
        """
        self.id: Optional[int] = None
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.date_of_birth: str = date_of_birth
        self.sex: str = sex
        self.ranking: int = ranking
        self.tournament_id: Optional[int] = None
        self.points: Optional[float] = None
        self.opponent_ids: List[Optional[int | None]] = []
        self.name: str = self.first_name + " " + self.last_name

    def __str__(self):
        """String representation of a player."""
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
        """Turns a player object into a dictionary.

        Returns:
            A dictionary of the player attributes.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "sex": self.sex,
            "ranking": self.ranking,
            "tournament_id": self.tournament_id,
            "points": self.points,
            "opponent_ids": self.opponent_ids
        }

    def save(self):
        """Saves or updates a player into a TinyDB database."""
        if self.id is None:
            self.id = players_table.insert(self.serialized)
            players_table.update({"id": self.id}, doc_ids=[self.id])
        else:
            players_table.update(self.serialized, doc_ids=[self.id])

    def set_ranking(self, ranking: int):
        """Updates the Elo ranking of a player."""
        self.ranking = ranking
        self.save()

    def reset(self):
        """
        Resets the points, the opponent_ids
        and the tournament_id attributes.
        """
        self.points = None
        self.opponent_ids = []
        self.tournament_id = None
        self.save()
