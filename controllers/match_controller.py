from tinydb import where

from typing import Optional

from models.match import Match
from views.match_view import MatchView
from controllers.player_controller import PlayerController


class MatchController():

    def __init__(
        self,
        match_view: MatchView,
        player_controller: PlayerController
    ):
        self.match_view: MatchView = match_view
        self.player_controller: PlayerController = player_controller

    def get_match_by_id(self, id) -> Optional[Match]:
        serialized_match = self.match_view.matches_table.get(where("id") == id)
        if serialized_match is None:
            return None
        id_player_1 = serialized_match["player_1"]["id"]
        id_player_2 = serialized_match["player_2"]["id"]
        player_1 = self.player_controller.get_player_by_id(id_player_1)
        player_2 = self.player_controller.get_player_by_id(id_player_2)
        score_1 = serialized_match["score_1"]
        score_2 = serialized_match["score_2"]
        match = Match(player_1, player_2)
        match.id = id
        match.score_1 = score_1
        match.score_2 = score_2
        return match

    def set_scores(self, match: Match, match_index):
        winner_id = self.match_view.get_winner_id(
            match_index,
            match.player_1.name,
            match.player_1.id,
            match.player_2.name,
            match.player_2.id
        )
        if match.score_1 is None:
            match.score_1 = 0
        if match.score_2 is None:
            match.score_2 = 0
        if match.player_1.points is None:
            match.player_1.points = 0
        if match.player_2.points is None:
            match.player_2.points = 0
        if winner_id == match.player_1.id:
            match.score_1 += 1
            match.player_1.points += 1
        elif winner_id == match.player_2.id:
            match.score_2 += 1
            match.player_2.points += 1
        else:
            match.score_1 += 0.5
            match.score_2 += 0.5
            match.player_1.points += 0.5
            match.player_2.points += 0.5
        match.save()
