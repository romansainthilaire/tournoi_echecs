from tinydb import where

from models.match import Match
from views.match_view import MatchView
from controllers.player_controller import PlayerController


class MatchController():

    def __init__(
        self,
        match_view: MatchView,
        player_controller: PlayerController
    ):
        self.match_view = match_view
        self.player_controller = player_controller

    def get_match_by_id(self, id) -> Match:
        serialized_match = self.match_view.matches_table.get(
            where("id") == id)  # type: ignore
        id_player_1 = serialized_match["player_1"]["id"]  # type: ignore
        id_player_2 = serialized_match["player_2"]["id"]  # type: ignore
        player_1 = self.player_controller.get_player_by_id(id_player_1)
        player_2 = self.player_controller.get_player_by_id(id_player_2)
        score_1 = serialized_match["score_1"]  # type: ignore
        score_2 = serialized_match["score_2"]  # type: ignore
        match = Match(player_1, player_2, score_1, score_2)
        match.id = id
        return match

    def set_scores(self, match: Match, match_index):
        player_1 = match.player_1
        player_2 = match.player_2
        winner_id = self.match_view.get_winner_id(
            match_index,
            player_1.name,
            player_1.id,
            player_2.name,
            player_2.id)
        if winner_id == player_1.id:
            match.score_1 += 1
            player_1.points += 1
        elif winner_id == player_2.id:
            match.score_2 += 1
            player_2.points += 1
        else:
            match.score_1 += 0.5
            match.score_2 += 0.5
            player_1.points += 0.5
            player_2.points += 0.5
        player_1.save()
        player_2.save()
        match.save()
