from datetime import datetime

from tinydb.table import Table


class PlayerView:
    """Gets player information from the user or shows player information to the user."""

    def __init__(self, players_table: Table):
        self.players_table: Table = players_table

    def get_player_id(self) -> int:
        """Gets a player id.

        Returns:
            The id of the player.
        """
        all_players = self.players_table.all()
        player_id = -1
        while True:
            try:
                player_id = int(input("\tID du joueur : "))
            except ValueError:
                continue
            if player_id not in [player['id'] for player in all_players]:
                print("\tCet ID ne correspond à aucun joueur.")
            else:
                break
        return player_id

    def get_first_name(self) -> str:
        """Gets the first name of a player.

        Returns:
            The first name of the player.
        """
        return input("\t- Prénom : ").title()

    def get_last_name(self) -> str:
        """Gets the last name of a player.

        Returns:
            The last name of the player.
        """
        return input("\t- Nom : ").upper()

    def get_date_of_birth(self) -> str:
        """Gets the date of birth of a player in the format DD/MM/YYYY.

        Returns:
            The date of birth of the player.
        """
        while True:
            date_of_birth = input("\t- Date de naissance (JJ/MM/AAAA) : ")
            try:
                date_of_birth = datetime.strptime(date_of_birth, "%d/%m/%Y")
                if date_of_birth > datetime.now():
                    print("\tLa date de naissance ne peut pas se situer dans le futur.")
                    continue
                break
            except ValueError:
                print("\tFormat de date invalide.")
                continue
        return date_of_birth.strftime("%d/%m/%Y")

    def get_sex(self) -> str:
        """Gets the sex of a player. The sex is either "M" or "F".

        Returns:
            The sex of the payer.
        """
        sex = ""
        while sex not in ["M", "F"]:
            sex = input("\t- Sexe (M/F): ").upper()
        return sex

    def get_ranking(self) -> int:
        """Gets the Elo ranking of a player. The ranking must be > 0.

        Returns:
            The Elo ranking of the player.
        """
        ranking = -1
        while ranking < 1:
            try:
                ranking = int(input("\t- Classement Elo : "))
            except ValueError:
                continue
        return ranking

    def get_new_ranking(self, player_name: str) -> int:
        """Gets a new Elo ranking for the player.

        Arguments:
            player_name -- name of the player

        Returns:
            The new Elo ranking.
        """
        new_ranking = -1
        while new_ranking < 1:
            try:
                new_ranking = int(input(f"\tNouveau classement Elo pour {player_name} : "))
            except ValueError:
                continue
        return new_ranking
