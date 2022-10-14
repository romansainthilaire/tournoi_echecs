from typing import List

from tinydb import where

from models.player import Player
from models.tournament import Tournament
from views.player_view import PlayerView


class PlayerController():

    def __init__(self, player_view: PlayerView):
        self.player_view: PlayerView = player_view

    def get_player_by_id(self, id: int) -> Player:
        """
        Gets a player object according to its id.
        The player attributes are extracted from the database.

        Arguments:
            id -- id of the player

        Returns:
            A player object.
        """
        serialized_player = self.player_view.players_table.get(where("id") == id)  # type: ignore
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
        """Gets a list of all the players.

        Returns:
            A list of all the players.
        """
        players = []
        serialized_players = self.player_view.players_table.all()
        for serialized_player in serialized_players:
            player = self.get_player_by_id(serialized_player["id"])
            players.append(player)
        return players

    def get_all_players_sorted_by_name(self) -> List[Player]:
        """Gets a list of all the players sorted by name.

        Returns:
            A list of all the players sorted by name.
        """
        players = self.get_all_players()
        return sorted(players, key=lambda player: player.name)

    def get_all_players_sorted_by_ranking(self) -> List[Player]:
        """Gets a list of all the players sorted by Elo ranking.

        Returns:
            A list of all the players sorted by Elo ranking.
        """
        players = self.get_all_players()
        return sorted(players, key=lambda player: (-player.ranking, player.name))

    def add_new_player(self):
        """Adds a new player to the database."""
        first_name = self.player_view.get_first_name()
        last_name = self.player_view.get_last_name()
        date_of_birth = self.player_view.get_date_of_birth()
        sex = self.player_view.get_sex()
        ranking = self.player_view.get_ranking()
        player = Player(first_name, last_name, date_of_birth, sex, ranking)
        player.save()

    def update_player_ranking(self) -> Player:
        """Updates the Elo ranking of a player.

        Returns:
            The player.
        """
        player_id = self.player_view.get_player_id()
        player = self.get_player_by_id(player_id)
        new_ranking = self.player_view.get_new_ranking(player.name)
        player.set_ranking(new_ranking)
        return player
