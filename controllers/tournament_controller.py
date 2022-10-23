from typing import List, Optional

from tinydb import where

from models.player import Player
from models.tournament import Tournament
from views.tournament_view import TournamentView
from controllers.player_controller import PlayerController
from controllers.round_controller import RoundController


class TournamentController():

    def __init__(
        self,
        tournament_view: TournamentView,
        player_controller: PlayerController,
        round_controller: RoundController
    ):
        self.tournament_view: TournamentView = tournament_view
        self.player_controller: PlayerController = player_controller
        self.round_controller: RoundController = round_controller

    def get_tournament_by_id(self, tournament_id: Optional[int]) -> Tournament:
        """
        Gets a tournament object according to its id.
        The tournament attributes are extracted from the database.

        Arguments:
            tournament_id -- id of the tournament

        Returns:
            A tournament object.
        """
        serialized_tournament = self.tournament_view.tournaments_table.get(
            where("id") == tournament_id  # type: ignore
        )
        if serialized_tournament is None:
            return Tournament("", "", "", "", "")
        name = serialized_tournament["name"]
        description = serialized_tournament["description"]
        location = serialized_tournament["location"]
        time_control = serialized_tournament["time_control"]
        date = serialized_tournament["date"]
        total_rounds = serialized_tournament["total_rounds"]
        rounds_completed = serialized_tournament["rounds_completed"]
        players = []
        for player_id in serialized_tournament["player_ids"]:
            player = self.player_controller.get_player_by_id(player_id)
            players.append(player)
        rounds = []
        for round_id in serialized_tournament["round_ids"]:
            round = self.round_controller.get_round_by_id(round_id)
            rounds.append(round)
        tournament = Tournament(name, description, location, time_control, date)
        tournament.id = tournament_id
        tournament.total_rounds = total_rounds
        tournament.rounds_completed = rounds_completed
        tournament.players = players
        tournament.rounds = rounds
        return tournament

    def get_all_tournaments(self) -> List[Tournament]:
        """Gets a list of all the tournaments.

        Returns:
            A list of all the tournaments.
        """
        tournaments = []
        serialized_tournaments = self.tournament_view.tournaments_table.all()
        for serialized_tournament in serialized_tournaments:
            tournament = self.get_tournament_by_id(serialized_tournament["id"])
            tournaments.append(tournament)
        return tournaments

    def get_active_tournaments(self) -> List[Tournament]:
        """Gets a list of the tournaments that are not finished yet.

        Returns:
            A list of active tournaments.
        """
        active_tournaments = []
        for tournament in self.get_all_tournaments():
            if tournament.rounds_completed < tournament.total_rounds:
                active_tournaments.append(tournament)
        return active_tournaments

    def get_active_tournament_ids(self) -> List[Optional[int]]:
        """Gets a list of the ids of the tournaments that are not finished yet.

        Returns:
            A list of active tournament ids.
        """
        return [tournament.id for tournament in self.get_active_tournaments()]

    def get_available_players(self) -> List[Player]:
        """Gets a list of the players that are not already playing in another tournament.

        Returns:
            A list of available players.
        """
        available_players = []
        for player in self.player_controller.get_all_players():
            if not self.player_in_active_tournament(player):
                available_players.append(player)
        return available_players

    def add_n_players_to_tournament(self, n: int, tournament: Tournament):
        """Adds players to a tournament.

        Arguments:
            n -- number of players to be added to the tournament
            tournament -- tournament object
            available_players -- players that are not already playing in another tournament
        """
        added_player_ids = []
        available_player_ids = [player.id for player in self.get_available_players()]
        for index in range(1, n + 1):
            player_id = self.tournament_view.get_player_id(index, added_player_ids, available_player_ids)
            player = self.player_controller.get_player_by_id(player_id)
            player.tournament_id = tournament.id
            tournament.add_player(player)
            added_player_ids.append(player.id)

    def add_new_tournament(self):
        """Creates a new tournament.

        Arguments:
            available_players -- players that are not already playing in another tournament
        """
        name = self.tournament_view.get_name()
        description = self.tournament_view.get_description()
        location = self.tournament_view.get_location()
        time_control = self.tournament_view.get_time_control()
        date = self.tournament_view.get_date()
        nb_available_players = len(self.get_available_players())
        nb_players = self.tournament_view.get_nb_players(nb_available_players)
        total_rounds = self.tournament_view.get_total_rounds(nb_players)
        tournament = Tournament(name, description, location, time_control, date)
        tournament.total_rounds = total_rounds
        tournament.save()  # add_n_players_to_tournament() requires a tournament with an id
        self.add_n_players_to_tournament(nb_players, tournament)
        tournament.save()

    def player_in_active_tournament(self, player: Player) -> bool:
        """Checks if a player alreary plays in another tournament.

        Arguments:
            player -- a player object

        Returns:
            True is the player alreary plays in another tournament.
        """
        return player.tournament_id in self.get_active_tournament_ids()
