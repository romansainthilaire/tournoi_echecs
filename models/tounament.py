from pathlib import Path
from datetime import date
from typing import List

from tinydb import TinyDB

from models.player import Player
from models.round import Round


db = TinyDB(Path(__file__).parent.parent / "db.json", indent=4)
tournaments_table = db.table("tournaments")


class Tournament():

    def __init__(
        self,
        name: str,
        description: str,
        location: str,
        time_control: str,
        day: int,
        month: int,
        year: int,
        nb_rounds: int = 4,
        players: List[Player] = [],
        rounds: List[Round] = []
    ):
        self.name = name
        self.description = description
        self.location = location
        self.time_control = time_control
        self.date = date(year, month, day)
        self.nb_rounds = nb_rounds
        self.players = players
        self.rounds = rounds

    @property
    def serialized(self):
        return {
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "time_control": self.time_control,
            "date": self.date.strftime("%d/%m/%Y"),
            "nb_rounds": self.nb_rounds,
            "players": [player.serialized for player in self.players],
            "rounds": [round.serialized for round in self.rounds],
        }

    def save(self):
        self.id = tournaments_table.insert(self.serialized)

    def add_player(self, player: Player):
        self.players.append(player)

    def add_round(self, round: Round):
        self.rounds.append(round)
