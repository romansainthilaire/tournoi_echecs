from datetime import datetime

from tinydb import where

from models.round import Round
from views.round_view import RoundView
from controllers.match_controller import MatchController


class RoundController():

    def __init__(
        self,
        round_view: RoundView,
        match_controller: MatchController
    ):
        self.round_view = round_view
        self.match_controller = match_controller

    def get_round_by_id(self, id) -> Round:
        serialized_round = self.round_view.rounds_table.get(
            where("id") == id)  # type: ignore
        name = serialized_round["name"]  # type: ignore
        matches = []
        for match in serialized_round["matches"]:  # type: ignore
            matches.append(self.match_controller.get_match_by_id(match["id"]))
        start = datetime.strptime(serialized_round["start"],  # type: ignore
                                  "%d/%m/%Y %H:%M:%S")
        end = datetime.strptime(serialized_round["end"],  # type: ignore
                                "%d/%m/%Y %H:%M:%S")
        in_progress = serialized_round["in_progress"]  # type: ignore
        round = Round(name, matches, start, end, in_progress)
        round.id = id
        return round
