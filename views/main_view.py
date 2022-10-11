class MainView():

    def print_menu(self):
        print("\n1.   Enregistrer un joueur")
        print("2.   Modifier le classement d'un joueur")
        print("3.   Afficher tous les joueurs par ordre alphabétique")
        print("4.   Afficher tous les joueurs par classement")
        print("5.   Créer un tournoi")
        print("6.   Afficher tous les tournois")
        print("7.   Afficher les joueurs d'un tournois par odre alphabétique")
        print("8.   Afficher les joueurs d'un tournois par classement")
        print("9.   Initialiser un round")
        print("10.  Rentrer les résultats d'un round")
        print("11.  Afficher les rounds d'un tournois")
        print("12.  Afficher les matchs d'un tournois")
        print("0.   Quitter")

    def get_action(self):
        action = -1
        while action not in range(13):
            try:
                action = int(input("\nAction : "))
            except ValueError:
                print("\nVeuillez entrer un nombre compris entre 0 et 12.")
                continue
            if action not in range(13):
                print("\nVeuillez entrer un nombre compris entre 0 et 12.")
        return action
