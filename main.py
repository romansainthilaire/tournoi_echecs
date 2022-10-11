from pathlib import Path

from tinydb import TinyDB

from views.player_view import PlayerView
from views.match_view import MatchView
from views.round_view import RoundView
from views.tournament_view import TournamentView
from views.main_view import MainView
from controllers.player_controller import PlayerController
from controllers.match_controller import MatchController
from controllers.round_controller import RoundController
from controllers.tournament_controller import TournamentController


db = TinyDB(Path(__file__).parent / "db.json", indent=4)

players_table = db.table("players")
matches_table = db.table("matches")
rounds_table = db.table("rounds")
tournaments_table = db.table("tournaments")

player_view = PlayerView(players_table)
match_view = MatchView(matches_table)
round_view = RoundView(rounds_table)
tournament_view = TournamentView(tournaments_table, players_table)
main_view = MainView()

player_controller = PlayerController(player_view)
match_controller = MatchController(match_view, player_controller)
round_controller = RoundController(round_view, match_controller)
tournament_controller = TournamentController(
    tournament_view,
    player_controller,
    round_controller
    )

action = -1
while action != 0:

    main_view.print_menu()
    action = main_view.get_action()

    if action == 1:
        print("\n\tNOUVEAU JOUEUR\n")
        player_controller.add_new_player()

    elif action == 2:
        all_players = player_controller.get_all_players()
        if len(all_players) == 0:
            print("\nOpération impossible : aucun joueur n'est enregistré.")
        else:
            print("\n\tMODIFICATION DU CLASSEMENT D'UN JOUEUR\n")
            player_controller.update_player_ranking()

    elif action == 3:
        all_players = player_controller.get_all_players_sorted_by_name()
        if len(all_players) == 0:
            print("\nOpération impossible : aucun joueur n'est enregistré.")
        else:
            print("\n\tTOUS LES JOUEURS\n\t→ Par ordre alphabétique")
            for player in all_players:
                print(player)

    elif action == 4:
        all_players = player_controller.get_all_players_sorted_by_ranking()
        if len(all_players) == 0:
            print("\nOpération impossible : aucun joueur n'est enregistré.")
        else:
            print("\n\tTOUS LES JOUEURS\n\t→ Par classement")
            for player in all_players:
                print(player)

    elif action == 5:
        all_players = player_controller.get_all_players()
        if len(all_players) == 0:
            print("\nOpération impossible : aucun joueur n'est enregistré.")
        elif len(all_players) < 4:
            print(
                "\nOpération impossible : " +
                "nombre de joueurs enregistrés insuffisant."
            )
        else:
            print("\n\tNOUVEAU TOURNOIS\n")
            tournament_controller.add_new_tournament()

    elif action == 6:
        all_tournaments = tournament_controller.get_all_tournaments()
        if len(all_tournaments) == 0:
            print("\nOpération impossible : aucun tournoi n'est enregistré.")
        else:
            print("\n\tTOUS LES TOURNOIS")
            for tournament in all_tournaments:
                print(tournament)

    elif action == 7:
        all_tournaments = tournament_controller.get_all_tournaments()
        if len(all_tournaments) == 0:
            print("\nOpération impossible : aucun tournoi n'est enregistré.")
        else:
            print()
            id = tournament_controller.tournament_view.get_id()
            tournament = tournament_controller.get_tournament_by_id(id)
            print(
                f"\n\tJOUEURS DU TOURNOI '{tournament.name}'"
                "\n\t→ Par ordre alphabétique"
            )
            players = tournament.get_players_sorted_by_name()
            for player in players:
                print(player)

    elif action == 8:
        all_tournaments = tournament_controller.get_all_tournaments()
        if len(all_tournaments) == 0:
            print("\nOpération impossible : aucun tournoi n'est enregistré.")
        else:
            print()
            id = tournament_controller.tournament_view.get_id()
            tournament = tournament_controller.get_tournament_by_id(id)
            print(
                f"\n\tJOUEURS DU TOURNOI '{tournament.name}'" +
                "\n\t→ Par classement"
            )
            players = tournament.get_players_sorted_by_name()
            for player in players:
                print(player)

    elif action == 9:
        all_tournaments = tournament_controller.get_all_tournaments()
        if len(all_tournaments) == 0:
            print("\nOpération impossible : aucun tournoi n'est enregistré.")
        else:
            print()
            id = tournament_controller.tournament_view.get_id()
            tournament = tournament_controller.get_tournament_by_id(id)
            if tournament.rounds != [] and tournament.rounds[-1].in_progress:
                print(
                    "\nOpération impossible : un round est déjà en "
                    "cours sur ce tournoi."
                )
            else:
                tournament.start_round()
                print(
                    f"\n\t{tournament.rounds[-1].name} initialisé."
                    f"\n\t→ {len(tournament.rounds[-1].matches)} matchs "
                    f"générés pour le tournoi '{tournament.name}'."
                )

    elif action == 10:
        all_tournaments = tournament_controller.get_all_tournaments()
        if len(all_tournaments) == 0:
            print("\nOpération impossible : aucun tournoi n'est enregistré.")
        else:
            print()
            id = tournament_controller.tournament_view.get_id()
            tournament = tournament_controller.get_tournament_by_id(id)
            if (
                tournament.rounds == [] or
                not tournament.rounds[-1].in_progress
            ):
                print(
                    "\nOpération impossible : " +
                    "aucun round n'a été initialisé pour ce tournoi."
                )
            else:
                matches = tournament.rounds[-1].matches
                print(
                    f"\n\tTournoi : {tournament.name}"
                    f"\n\n\tRésultats du {tournament.rounds[-1].name} :"
                )
                for index, match in enumerate(matches):
                    match_controller.set_scores(match, index + 1)
                tournament.finish_round()

    elif action == 11:
        all_tournaments = tournament_controller.get_all_tournaments()
        if len(all_tournaments) == 0:
            print("\nOpération impossible : aucun tournoi n'est enregistré.")
        else:
            print()
            id = tournament_controller.tournament_view.get_id()
            tournament = tournament_controller.get_tournament_by_id(id)
            if tournament.rounds == []:
                print(
                    "\nOpération impossible : " +
                    "aucun round n'a été initialisé pour ce tournoi."
                )
            else:
                print(f"\n\tTournoi : {tournament.name}")
                for round in tournament.rounds:
                    print(round)

    elif action == 12:
        all_tournaments = tournament_controller.get_all_tournaments()
        if len(all_tournaments) == 0:
            print("\nOpération impossible : aucun tournoi n'est enregistré.")
        else:
            print()
            id = tournament_controller.tournament_view.get_id()
            tournament = tournament_controller.get_tournament_by_id(id)
            if tournament.rounds == []:
                print(
                    "\nOpération impossible : " +
                    "aucun round n'a été initialisé pour ce tournoi."
                )
            else:
                print(f"\n\tTournoi : {tournament.name}")
                for round in tournament.rounds:
                    for match in round.matches:
                        print(match)
