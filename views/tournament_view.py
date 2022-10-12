from datetime import datetime

from typing import List

from tinydb.table import Table


class TournamentView:

    def __init__(
        self,
        tournaments_table: Table,
        players_table: Table
    ):
        self.tournaments_table: Table = tournaments_table
        self.players_table: Table = players_table

    def get_id(self) -> int:
        tournaments = self.tournaments_table.all()
        id = -1
        while True:
            try:
                id = int(input("\tID du tournoi : "))
            except ValueError:
                continue
            if id not in [tournament['id'] for tournament in tournaments]:
                print("\tCet ID ne correspond à aucun tournoi.")
            else:
                break
        return id

    def get_name(self) -> str:
        return input("\t- Nom du tournoi : ")

    def get_description(self) -> str:
        return input("\t- Description : ")

    def get_location(self) -> str:
        return input("\t- Lieu : ")

    def get_time_control(self) -> str:
        time_control = ""
        while time_control not in ["bullet", "blitz", "coup rapide"]:
            time_control = input(
                "\t- Contrôle du temps (bullet/blitz/coup rapide) : "
            ).lower()
        return time_control

    def get_date(self) -> str:
        while True:
            date = input("\t- Date (JJ/MM/AAAA) : ")
            try:
                date = datetime.strptime(date, "%d/%m/%Y")
                break
            except ValueError:
                print("\tFormat de date invalide.")
                continue
        return date.strftime("%d/%m/%Y")

    def get_nb_players(self, nb_available_players: int) -> int:
        nb_players = -1
        while (
            nb_players < 4 or
            nb_players % 2 != 0 or
            nb_players > nb_available_players
        ):
            try:
                nb_players = int(input("\t- Nombre de joueurs : "))
            except ValueError:
                continue
            if -1 < nb_players < 4:
                print("\tNombre minimum de joueurs : 4")
            elif nb_players > nb_available_players:
                print("\tNombre de joueurs disponibles insuffisant.")
            elif nb_players > 4 and nb_players % 2 != 0:
                print("\tNombre impair de joueurs.")
        return nb_players

    def get_total_rounds(self, nb_players: int) -> int:
        nb_max_rounds = nb_players - 1
        nb_rounds = -1
        while nb_rounds < 1 or nb_rounds > nb_max_rounds:
            try:
                nb_rounds = int(input("\t- Nombre de rounds : "))
            except ValueError:
                continue
            if nb_rounds > nb_max_rounds:
                print(
                    f"\tNombre de rounds maximal pour {nb_players} joueurs : "
                    f"{nb_max_rounds}"
                )
        return nb_rounds

    def get_player_id(
        self,
        index: int,
        added_player_ids: List[int],
        available_player_ids: List[int]
    ) -> int:
        id = -1
        while True:
            try:
                id = int(input(f"\t\t→ ID Joueur {index} : "))
            except ValueError:
                continue
            if id not in [player['id'] for player in self.players_table.all()]:
                print("\t\tCet ID ne correspond à aucun joueur.")
            elif id not in available_player_ids:
                print(
                    "\t\tCet ID n'est pas disponible "
                    "(joueur déjà pris sur un autre tournois)."
                )
            elif id in added_player_ids:
                print("\t\tVous avez déjà ajouté ce joueur.")
            else:
                break
        return id
