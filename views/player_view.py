from datetime import datetime

from tinydb.table import Table


class PlayerView:

    def __init__(self, players_table: Table):
        self.players_table: Table = players_table

    def get_id(self) -> int:
        players = self.players_table.all()
        id = -1
        while True:
            try:
                id = int(input("\tID du joueur : "))
            except ValueError:
                continue
            if id not in [player['id'] for player in players]:
                print("\tCet ID ne correspond à aucun joueur.")
            else:
                break
        return id

    def get_first_name(self) -> str:
        return input("\t- Prénom : ").title()

    def get_last_name(self) -> str:
        return input("\t- Nom : ").upper()

    def get_date_of_birth(self) -> str:
        while True:
            birth_date = input("\t- Date de naissance (JJ/MM/AAAA) : ")
            try:
                birth_date = datetime.strptime(birth_date, "%d/%m/%Y")
                break
            except ValueError:
                print("\tFormat de date invalide.")
                continue
        return birth_date.strftime("%d/%m/%Y")

    def get_sex(self) -> str:
        sex = ""
        while sex not in ["M", "F"]:
            sex = input("\t- Sexe (M/F): ").upper()
        return sex

    def get_ranking(self) -> int:
        ranking = -1
        while ranking < 1:
            try:
                ranking = int(input("\t- Classement Elo : "))
            except ValueError:
                continue
        return ranking

    def get_new_ranking(self, player_name: str) -> int:
        ranking = -1
        while ranking < 1:
            try:
                ranking = int(input(
                    f"\tNouveau classement Elo pour {player_name} : "
                ))
            except ValueError:
                continue
        return ranking
