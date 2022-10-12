from datetime import datetime
from typing import Optional

from tinydb.table import Table
from tinydb import where

from models.round import Round
from controllers.match_controller import MatchController


class RoundController():

    def __init__(
        self,
        rounds_table: Table,
        match_controller: MatchController
    ):
        self.rounds_table: Table = rounds_table
        self.match_controller: MatchController = match_controller

    def get_round_by_id(self, id) -> Optional[Round]:
        serialized_round = self.rounds_table.get(where("id") == id)
        if serialized_round is None:
            return None
        name = serialized_round["name"]
        matches = []
        for match in serialized_round["matches"]:
            matches.append(self.match_controller.get_match_by_id(match["id"]))
        start = datetime.strptime(serialized_round["start"], Round.DATE_FORMAT)
        end = datetime.strptime(serialized_round["end"], Round.DATE_FORMAT)
        in_progress = serialized_round["in_progress"]
        round = Round(name)
        round.matches = matches
        round.start = start
        round.end = end
        round.in_progress = in_progress
        round.id = id
        return round
