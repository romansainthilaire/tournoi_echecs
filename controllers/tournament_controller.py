from typing import List

from tinydb import where

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
        self.tournament_view = tournament_view
        self.player_controller = player_controller
        self.round_controller = round_controller

    def get_tournament_by_id(self, id) -> Tournament:
        serialized_tournament = self.tournament_view.tournaments_table.get(
            where("id") == id)  # type: ignore
        name = serialized_tournament["name"]  # type: ignore
        description = serialized_tournament["description"]  # type: ignore
        location = serialized_tournament["location"]  # type: ignore
        time_control = serialized_tournament["time_control"]  # type: ignore
        date = serialized_tournament["date"]  # type: ignore
        total_rounds = serialized_tournament["total_rounds"]  # type: ignore
        rounds_comp = serialized_tournament["rounds_completed"]  # type: ignore
        players = []
        for player in serialized_tournament["players"]:  # type: ignore
            player = self.player_controller.get_player_by_id(player["id"])
            players.append(player)
        rounds = []
        for round in serialized_tournament["rounds"]:  # type: ignore
            round = self.round_controller.get_round_by_id(round["id"])
            rounds.append(round)
        tournament = Tournament(
            name,
            description,
            location,
            time_control,
            date
        )
        tournament.total_rounds = total_rounds
        tournament.rounds_completed = rounds_comp
        tournament.players = players
        tournament.rounds = rounds
        tournament.id = id
        return tournament

    def get_all_tournaments(self) -> List[Tournament]:
        tournaments = []
        serialized_tournaments = self.tournament_view.tournaments_table.all()
        for serialized_tournament in serialized_tournaments:
            tournament = self.get_tournament_by_id(serialized_tournament["id"])
            tournaments.append(tournament)
        return tournaments

    def add_players_to_tournament(self, n: int, tournament: Tournament):
        added_player_ids = []
        for index in range(1, n + 1):
            player_id = self.tournament_view.get_player_id(
                index,
                added_player_ids
            )
            player = self.player_controller.get_player_by_id(player_id)
            player.points = 0
            player.opponent_ids = []
            player.save()
            added_player_ids.append(player.id)
            tournament.add_player(player)

    def add_new_tournament(self):
        name = self.tournament_view.get_name()
        description = self.tournament_view.get_description()
        location = self.tournament_view.get_location()
        time_control = self.tournament_view.get_time_control()
        date = self.tournament_view.get_date()
        nb_players = self.tournament_view.get_nb_players()
        total_rounds = self.tournament_view.get_total_rounds(nb_players)
        tournament = Tournament(
            name,
            description,
            location,
            time_control,
            date
        )
        tournament.total_rounds = total_rounds
        self.add_players_to_tournament(nb_players, tournament)
        tournament.save()
