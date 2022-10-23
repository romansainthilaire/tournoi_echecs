class MainView():

    def print_menu(self):
        print("\n1.   Enregistrer un joueur")
        print("2.   Modifier le classement Elo d'un joueur")
        print("3.   Afficher tous les joueurs par ordre alphabétique")
        print("4.   Afficher tous les joueurs par classement Elo")
        print("5.   Créer un tournoi")
        print("6.   Afficher tous les tournois")
        print("7.   Afficher les joueurs d'un tournois par ordre alphabétique")
        print("8.   Afficher les joueurs d'un tournois par classement Elo")
        print("9.   Afficher les joueurs d'un tournois par points")
        print("10.  Initialiser un round")
        print("11.  Rentrer les résultats d'un round")
        print("12.  Afficher les rounds d'un tournois")
        print("13.  Afficher les matchs d'un tournois")
        print("0.   Quitter")

    def get_action(self):
        """Gets the action number.

        Returns:
            The action number.
        """
        action = -1
        while action not in range(14):
            try:
                action = int(input("\nAction : "))
            except ValueError:
                print("\nVeuillez entrer un nombre compris entre 0 et 13.")
                continue
            if action not in range(13):
                print("\nVeuillez entrer un nombre compris entre 0 et 13.")
        return action

    # HEADLINES

    def print_new_player_headline(self):
        print("\n\tNOUVEAU JOUEUR\n")

    def print_player_ranking_update_headline(self):
        print("\n\tMODIFICATION DU CLASSEMENT D'UN JOUEUR\n")

    def print_all_players_sorted_by_name_headline(self):
        print("\n\tTOUS LES JOUEURS\n\t→ Par ordre alphabétique")

    def print_all_players_sorted_by_ranking_headline(self):
        print("\n\tTOUS LES JOUEURS\n\t→ Par classement Elo")

    def print_new_tournament_headline(self):
        print("\n\tNOUVEAU TOURNOIS\n")

    def print_all_tournaments_headline(self):
        print("\n\tTOUS LES TOURNOIS")

    def print_tournament_players_sorted_by_name_headline(self, tournament_name: str):
        print(
            f"\n\tJOUEURS DU TOURNOI '{tournament_name}'"
            "\n\t→ Par ordre alphabétique"
        )

    def print_tournament_players_sorted_by_ranking_headline(self, tournament_name: str):
        print(
            f"\n\tJOUEURS DU TOURNOI '{tournament_name}'"
            "\n\t→ Par classement Elo"
        )

    def print_tournament_players_sorted_by_points_headline(self, tournament_name: str):
        print(
            f"\n\tJOUEURS DU TOURNOI '{tournament_name}'"
            "\n\t→ Par points"
        )

    def print_started_round_info(self, round_name: str, nb_matches: int, tournament_name: str):
        print(
            f"\n\t{round_name} initialisé."
            f"\n\n\t→ {nb_matches} matchs "
            f"générés pour le tournoi '{tournament_name}'."
        )

    def print_tournament_results_headline(self, tournament_name: str, round_name: str):
        print(
            f"\n\tTournoi : {tournament_name}"
            f"\n\n\tRésultats du {round_name} :"
        )

    def print_tournament_rounds_headline(self, tournament_name: str):
        print(f"\n\tROUNDS DU TOURNOI '{tournament_name}'")

    def print_tournament_matches_headline(self, tournament_name: str):
        print(f"\n\tMATCHS DU TOURNOI '{tournament_name}'")

    # ERROR MESSAGES

    def print_no_player_error(self):
        print("\nOpération impossible : aucun joueur n'est enregistré.")

    def print_no_tournament_error(self):
        print("\nOpération impossible : aucun tournoi n'est enregistré.")

    def print_not_enougth_players_error(self):
        print("\nOpération impossible : nombre de joueurs enregistrés insuffisant.")

    def print_not_enougth_available_players_error(self):
        print("\nOpération impossible : nombre de joueurs disponibles insuffisant.")

    def print_round_in_progress_error(self, tournament_name: str):
        print(f"\nOpération impossible : un round est déjà en cours sur le tournoi '{tournament_name}'.")

    def print_no_round_in_progress_error(self, tournament_name: str):
        print(f"\nOpération impossible : aucun round en cours sur le tournoi '{tournament_name}'.")

    def print_no_round_error(self, tournament_name: str):
        print(f"\nOpération impossible : aucun round n'a été initialisé pour le tournois '{tournament_name}'.")

    def print_tournament_finished_error(self, tournament_name: str):
        print(f"\nOpération impossible : le tournoi '{tournament_name}' est terminé.")
