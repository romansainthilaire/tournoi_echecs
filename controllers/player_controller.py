from typing import List

from tinydb import where

from models.player import Player
from views.player_view import PlayerView


class PlayerController():

    def __init__(self, player_view: PlayerView):
        self.player_view: PlayerView = player_view

    def get_player_by_id(self, id) -> Player:
        serialized_player = self.player_view.players_table.get(
            where("id") == id
        )
        if serialized_player is None:
            return Player("", "", "", "", 0)
        first_name = serialized_player["first_name"]
        last_name = serialized_player["last_name"]
        date_of_birth = serialized_player["date_of_birth"]
        sex = serialized_player["sex"]
        ranking = serialized_player["ranking"]
        tournament_id = serialized_player["tournament_id"]
        points = serialized_player["points"]
        opponent_ids = serialized_player["opponent_ids"]
        player = Player(first_name, last_name, date_of_birth, sex, ranking)
        player.id = id
        player.tournament_id = tournament_id
        player.points = points
        player.opponent_ids = opponent_ids
        return player

    def get_all_players(self) -> List[Player]:
        players = []
        serialized_players = self.player_view.players_table.all()
        for serialized_player in serialized_players:
            player = self.get_player_by_id(serialized_player["id"])
            players.append(player)
        return players

    def get_all_players_sorted_by_name(self) -> List[Player]:
        players = self.get_all_players()
        return sorted(
            players,
            key=lambda player: player.name
        )

    def get_all_players_sorted_by_ranking(self) -> List[Player]:
        players = self.get_all_players()
        return sorted(
            players,
            key=lambda player: (-player.ranking, player.name)
        )

    def add_new_player(self):
        first_name = self.player_view.get_first_name()
        last_name = self.player_view.get_last_name()
        date_of_birth = self.player_view.get_date_of_birth()
        sex = self.player_view.get_sex()
        ranking = self.player_view.get_ranking()
        player = Player(first_name, last_name, date_of_birth, sex, ranking)
        player.save()

    def update_player_ranking(self):
        player_id = self.player_view.get_id()
        player = self.get_player_by_id(player_id)
        new_ranking = self.player_view.get_new_ranking(player.name)
        player.set_ranking(new_ranking)
