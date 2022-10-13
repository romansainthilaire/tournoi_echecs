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

    def get_tournament_by_id(self, id) -> Tournament:
        serialized_tournament = self.tournament_view.tournaments_table.get(
            where("id") == id
        )
        if serialized_tournament is None:
            return Tournament("", "", "", "", "")
        name = serialized_tournament["name"]
        description = serialized_tournament["description"]
        location = serialized_tournament["location"]
        time_control = serialized_tournament["time_control"]
        date = serialized_tournament["date"]
        total_rounds = serialized_tournament["total_rounds"]
        rounds_comp = serialized_tournament["rounds_completed"]
        players = []
        for player in serialized_tournament["players"]:
            player = self.player_controller.get_player_by_id(player["id"])
            players.append(player)
        rounds = []
        for round in serialized_tournament["rounds"]:
            round = self.round_controller.get_round_by_id(round["id"])
            rounds.append(round)
        tournament = Tournament(
            name,
            description,
            location,
            time_control,
            date
        )
        tournament.id = id
        tournament.total_rounds = total_rounds
        tournament.rounds_completed = rounds_comp
        tournament.players = players
        tournament.rounds = rounds
        return tournament

    def get_all_tournaments(self) -> List[Tournament]:
        tournaments = []
        serialized_tournaments = self.tournament_view.tournaments_table.all()
        for serialized_tournament in serialized_tournaments:
            tournament = self.get_tournament_by_id(serialized_tournament["id"])
            tournaments.append(tournament)
        return tournaments

    def get_active_tournaments(self) -> List[Tournament]:
        active_tournaments = []
        for tournament in self.get_all_tournaments():
            if tournament.rounds_completed < tournament.total_rounds:
                active_tournaments.append(tournament)
        return active_tournaments

    def get_active_tournament_ids(self) -> List[Optional[int | None]]:
        return [tournament.id for tournament in self.get_active_tournaments()]

    def add_players_to_tournament(
        self, n: int,
        tournament: Tournament,
        available_players: List[Player]
    ):
        added_player_ids = []
        available_player_ids = [player.id for player in available_players]
        for index in range(1, n + 1):
            player_id = self.tournament_view.get_player_id(
                index,
                added_player_ids,
                available_player_ids
            )
            player = self.player_controller.get_player_by_id(player_id)
            player.tournament_id = tournament.id
            tournament.add_player(player)
            added_player_ids.append(player.id)

    def add_new_tournament(self, available_players: List[Player]):
        name = self.tournament_view.get_name()
        description = self.tournament_view.get_description()
        location = self.tournament_view.get_location()
        time_control = self.tournament_view.get_time_control()
        date = self.tournament_view.get_date()
        nb_available_players = len(available_players)
        nb_players = self.tournament_view.get_nb_players(nb_available_players)
        total_rounds = self.tournament_view.get_total_rounds(nb_players)
        tournament = Tournament(
            name,
            description,
            location,
            time_control,
            date
        )
        tournament.total_rounds = total_rounds
        tournament.save()
        self.add_players_to_tournament(
            nb_players,
            tournament,
            available_players
        )
        tournament.save()

    def player_in_active_tournament(self, player: Player) -> bool:
        return player.tournament_id in self.get_active_tournament_ids()

    def get_available_players(self) -> List[Player]:
        available_players = []
        for player in self.player_controller.get_all_players():
            if not self.player_in_active_tournament(player):
                available_players.append(player)
        return available_players
