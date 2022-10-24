from datetime import datetime

from typing import List, Optional

from tinydb import where
from tinydb.table import Table


class TournamentView:
    """Gets tournament information from the user or shows tournament information to the user."""

    def __init__(self, tournaments_table: Table, players_table: Table):
        self.tournaments_table: Table = tournaments_table
        self.players_table: Table = players_table

    def get_tournament_id(self) -> int:
        """Gets a tournament id.

        Returns:
            The id of the tournament.
        """
        all_tournaments = self.tournaments_table.all()
        tournament_id = -1
        while True:
            try:
                tournament_id = int(input("\tID du tournoi : "))
            except ValueError:
                continue
            if tournament_id not in [tournament['id'] for tournament in all_tournaments]:
                print("\tCet ID ne correspond à aucun tournoi.")
            else:
                break
        return tournament_id

    def get_name(self) -> str:
        """Gets the name of a tournament.

        Returns:
            The name of the tournament.
        """
        name = input("\t- Nom du tournoi : ")
        return name.title()

    def get_description(self) -> str:
        """Gets the description of a tournament.

        Returns:
            The description of the tournament.
        """
        description = input("\t- Description : ")
        return description[0].upper() + description[1:]

    def get_location(self) -> str:
        """Gets the location of a tournament.

        Returns:
            The location of the tournament.
        """
        location = input("\t- Lieu : ")
        return location[0].upper() + location[1:]

    def get_time_control(self) -> str:
        """
        Gets the time control type of a tournament.
        The time control type must be either "bullet", "blitz" or "coup rapide".

        Returns:
            The time control type of the tournament.
        """
        time_control = ""
        while time_control not in ["bullet", "blitz", "coup rapide"]:
            time_control = input("\t- Contrôle du temps (bullet/blitz/coup rapide) : ")
        return time_control.lower()

    def get_date(self) -> str:
        """Gets the starting date of a tournament in the format DD/MM/YYYY.

        Returns:
            The starting date of the tournament.
        """
        while True:
            date = input("\t- Date (JJ/MM/AAAA) : ")
            try:
                date = datetime.strptime(date, "%d/%m/%Y")
                if date < datetime.now():
                    print("\tLa date du tournoi ne peut pas se situer dans le passé.")
                    continue
                break
            except ValueError:
                print("\tFormat de date invalide.")
                continue
        return date.strftime("%d/%m/%Y")

    def get_nb_players(self, nb_available_players: int) -> int:
        """Gets the number of tournament participants.

        Arguments:
            nb_available_players -- number of players that are not already playing in another tournament

        Returns:
            The number of participants.
        """
        nb_players = -1
        while nb_players < 2 or nb_players % 2 != 0 or nb_players > nb_available_players:
            try:
                nb_players = int(input("\t- Nombre de joueurs : "))
            except ValueError:
                continue
            if nb_players > nb_available_players:
                print("\tNombre de joueurs disponibles insuffisant.")
            elif nb_players > 0 and nb_players % 2 != 0:
                print("\tNombre impair de joueurs.")
        return nb_players

    def get_total_rounds(self, nb_players: int) -> int:
        """Gets the total number of rounds of a tournament.

        Arguments:
            nb_players -- number of tournament participants

        Returns:
            The total number of rounds.
        """
        nb_max_rounds = 1 if nb_players == 2 else int(nb_players / 2 + 1)
        nb_rounds = -1
        while nb_rounds < 1 or nb_rounds > nb_max_rounds:
            try:
                nb_rounds = int(input("\t- Nombre de rounds : "))
            except ValueError:
                continue
            if nb_rounds > nb_max_rounds:
                print(f"\tNombre de rounds maximum pour {nb_players} joueurs : {nb_max_rounds}")
        return nb_rounds

    def get_player_id(
        self,
        index: int,
        added_player_ids: List[int],
        available_player_ids: List[Optional[int]]
    ) -> int:
        """Gets the id of a player, in order to create a new tournament.

        Arguments:
            index -- index of the player (for displaying purpose)
            added_player_ids -- ids of the players that are already added to the tournament
            available_player_ids -- ids of the players that are not already playing in another tournament

        Returns:
            The id of the player.
        """
        player_id = -1
        while True:
            try:
                player_id = int(input(f"\t\t→ ID Joueur {index} : "))
            except ValueError:
                continue
            if player_id not in [player['id'] for player in self.players_table.all()]:
                print("\t\tCet ID ne correspond à aucun joueur.")
            elif player_id not in available_player_ids:
                print("\t\tCet ID n'est pas disponible (joueur déjà pris sur un autre tournois).")
            elif player_id in added_player_ids:
                print("\t\tVous avez déjà ajouté ce joueur.")
            else:
                break
        return player_id

    def get_players_info(self, tournament_id: Optional[int]) -> List[dict]:
        """Gets the information of all players from a tournament.

        Arguments:
            tournament_id -- id of the tournament

        Returns:
            The information (list of dictionary) of the tournament players.
        """
        serialized_tournament = self.tournaments_table.get(where("id") == tournament_id)  # type: ignore
        player_ids = serialized_tournament["player_ids"]  # type: ignore
        serialized_players = []
        for player_id in player_ids:
            serialized_player = self.players_table.get(where("id") == player_id)  # type: ignore
            serialized_players.append(serialized_player)
        player_points = serialized_tournament["player_points"]  # type: ignore
        players_info = []
        for serialized_player, points in zip(serialized_players, player_points):
            first_name = serialized_player["first_name"]
            last_name = serialized_player["last_name"]
            ranking = serialized_player["ranking"]
            points = points if points is not None else 0
            info = (
                f"\nID {serialized_player['id']}"
                f"\t{first_name} {last_name} ({serialized_player['sex']})"
                f"\n\tNé le {serialized_player['date_of_birth']}"
                f"\n\tClassement Elo : {ranking}"
                f"\n\tPoints : {points}"
            )
            players_info.append({
                "first_name": first_name,
                "last_name": last_name,
                "ranking": ranking,
                "points": points,
                "info": info
            })
        return players_info

    def print_players_sorted_by_last_name(self, tournament_id: Optional[int]):
        """Prints tournament players sorted by last name.

        Arguments:
            tournament_id -- id of the tournament
        """
        players_info = sorted(
            self.get_players_info(tournament_id),
            key=lambda player_info: (player_info["last_name"], player_info["first_name"])
        )
        for player_info in players_info:
            print(player_info["info"])

    def print_players_sorted_by_ranking(self, tournament_id: Optional[int]):
        """Prints tournament players sorted by ranking.

        Arguments:
            tournament_id -- id of the tournament
        """
        players_info = sorted(
            self.get_players_info(tournament_id),
            key=lambda player_info: (-player_info["ranking"], player_info["last_name"], player_info["first_name"])
        )
        for player_info in players_info:
            print(player_info["info"])

    def print_players_sorted_by_points(self, tournament_id: Optional[int]):
        """Prints tournament players sorted by points.

        Arguments:
            tournament_id -- id of the tournament
        """
        players_info = sorted(
            self.get_players_info(tournament_id),
            key=lambda player_info: (-player_info["points"], -player_info["ranking"])
        )
        for player_info in players_info:
            print(player_info["info"])
