from datetime import datetime
from typing import Optional

from tinydb import where

from models.round import Round
from views.round_view import RoundView
from controllers.match_controller import MatchController


class RoundController():

    def __init__(self, round_view: RoundView, match_controller: MatchController):
        self.round_view: RoundView = round_view
        self.match_controller: MatchController = match_controller

    def get_round_by_id(self, id: int) -> Optional[Round]:
        """
        Gets a round object according to its id.
        The round attributes are extracted from the database.

        Arguments:
            id -- id of the round

        Returns:
            A round object.
        """
        serialized_round = self.round_view.rounds_table.get(where("id") == id)  # type: ignore
        if serialized_round is None:
            return None
        name = serialized_round["name"]
        matches = []
        for match in serialized_round["matches"]:
            matches.append(self.match_controller.get_match_by_id(match["id"]))
        start = datetime.strptime(serialized_round["start"], Round.DATETIME_FORMAT)
        end = datetime.strptime(serialized_round["end"], Round.DATETIME_FORMAT)
        in_progress = serialized_round["in_progress"]
        round = Round(name)
        round.id = id
        round.matches = matches
        round.start = start
        round.end = end
        round.in_progress = in_progress
        return round
