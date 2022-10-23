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

# DATABASE TABLES
players_table = db.table("players")
matches_table = db.table("matches")
rounds_table = db.table("rounds")
tournaments_table = db.table("tournaments")

# VIEWS
player_view = PlayerView(players_table)
match_view = MatchView(matches_table)
round_view = RoundView(rounds_table)
tournament_view = TournamentView(tournaments_table, players_table)
main_view = MainView()

# CONTROLLERS
player_controller = PlayerController(player_view)
match_controller = MatchController(match_view, player_controller)
round_controller = RoundController(round_view, match_controller)
tournament_controller = TournamentController(tournament_view, player_controller, round_controller)

if __name__ == "__main__":

    action = -1
    while action != 0:

        main_view.print_menu()
        action = main_view.get_action()

        if action == 1:
            main_view.print_new_player_headline()
            player_controller.add_new_player()

        elif action == 2:
            all_players = player_controller.get_all_players()
            if all_players == []:
                main_view.print_no_player_error()
            else:
                main_view.print_player_ranking_update_headline()
                player = player_controller.update_player_ranking()
                if player.tournament_id:
                    tounament_id = player.tournament_id
                    tournament = tournament_controller.get_tournament_by_id(tounament_id)
                    tournament.save()

        elif action == 3:
            all_players_sorted_by_name = player_controller.get_all_players_sorted_by_name()
            if all_players_sorted_by_name == []:
                main_view.print_no_player_error()
            else:
                main_view.print_all_players_sorted_by_name_headline()
                for player in all_players_sorted_by_name:
                    print(player)

        elif action == 4:
            all_players_sorted_by_ranking = player_controller.get_all_players_sorted_by_ranking()
            if all_players_sorted_by_ranking == []:
                main_view.print_no_player_error()
            else:
                main_view.print_all_players_sorted_by_ranking_headline()
                for player in all_players_sorted_by_ranking:
                    print(player)

        elif action == 5:
            all_players = player_controller.get_all_players()
            available_players = tournament_controller.get_available_players()
            if all_players == []:
                main_view.print_no_player_error()
            elif len(available_players) < 2:
                main_view.print_not_enougth_available_players_error()
            else:
                main_view.print_new_tournament_headline()
                tournament_controller.add_new_tournament()

        elif action == 6:
            all_tournaments = tournament_controller.get_all_tournaments()
            if all_tournaments == []:
                main_view.print_no_tournament_error()
            else:
                main_view.print_all_tournaments_headline()
                for tournament in all_tournaments:
                    print(tournament)

        elif action == 7:
            all_tournaments = tournament_controller.get_all_tournaments()
            if all_tournaments == []:
                main_view.print_no_tournament_error()
            else:
                print()
                tournament_id = tournament_controller.tournament_view.get_tournament_id()
                tournament = tournament_controller.get_tournament_by_id(tournament_id)
                main_view.print_tournament_players_sorted_by_name_headline(tournament.name)
                tournament_controller.tournament_view.print_players_sorted_by_name(tournament.id)

        elif action == 8:
            all_tournaments = tournament_controller.get_all_tournaments()
            if all_tournaments == []:
                main_view.print_no_tournament_error()
            else:
                print()
                tournament_id = tournament_controller.tournament_view.get_tournament_id()
                tournament = tournament_controller.get_tournament_by_id(tournament_id)
                main_view.print_tournament_players_sorted_by_ranking_headline(tournament.name)
                tournament_controller.tournament_view.print_players_sorted_by_ranking(tournament.id)

        elif action == 9:
            all_tournaments = tournament_controller.get_all_tournaments()
            if all_tournaments == []:
                main_view.print_no_tournament_error()
            else:
                print()
                tournament_id = tournament_controller.tournament_view.get_tournament_id()
                tournament = tournament_controller.get_tournament_by_id(tournament_id)
                main_view.print_tournament_players_sorted_by_points_headline(tournament.name)
                tournament_controller.tournament_view.print_players_sorted_by_points(tournament.id)

        elif action == 10:
            all_tournaments = tournament_controller.get_all_tournaments()
            if all_tournaments == []:
                main_view.print_no_tournament_error()
            else:
                print()
                tournament_id = tournament_controller.tournament_view.get_tournament_id()
                tournament = tournament_controller.get_tournament_by_id(tournament_id)
                if tournament.rounds != [] and tournament.rounds[-1].in_progress:
                    main_view.print_round_in_progress_error(tournament.name)
                elif tournament.rounds_completed == tournament.total_rounds:
                    main_view.print_tournament_finished_error(tournament.name)
                else:
                    tournament.start_round()
                    round = tournament.rounds[-1]
                    main_view.print_started_round_info(round.name, len(round.matches), tournament.name)

        elif action == 11:
            all_tournaments = tournament_controller.get_all_tournaments()
            if all_tournaments == []:
                main_view.print_no_tournament_error()
            else:
                print()
                tournament_id = tournament_controller.tournament_view.get_tournament_id()
                tournament = tournament_controller.get_tournament_by_id(tournament_id)
                if tournament.rounds == []:
                    main_view.print_no_round_error(tournament.name)
                elif not tournament.rounds[-1].in_progress:
                    main_view.print_no_round_in_progress_error(tournament.name)
                else:
                    round = tournament.rounds[-1]
                    main_view.print_tournament_results_headline(tournament.name, round.name)
                    for index, match in enumerate(round.matches):
                        f"\n\tMatch {index + 1}"
                        match_controller.set_scores(match)
                    tournament.finish_round()

        elif action == 12:
            all_tournaments = tournament_controller.get_all_tournaments()
            if all_tournaments == []:
                main_view.print_no_tournament_error()
            else:
                print()
                tournament_id = tournament_controller.tournament_view.get_tournament_id()
                tournament = tournament_controller.get_tournament_by_id(tournament_id)
                if tournament.rounds == []:
                    main_view.print_no_round_error(tournament.name)
                else:
                    main_view.print_tournament_rounds_headline(tournament.name)
                    for round in tournament.rounds:
                        print(round)

        elif action == 13:
            all_tournaments = tournament_controller.get_all_tournaments()
            if all_tournaments == []:
                main_view.print_no_tournament_error()
            else:
                print()
                tournament_id = tournament_controller.tournament_view.get_tournament_id()
                tournament = tournament_controller.get_tournament_by_id(tournament_id)
                if tournament.rounds == []:
                    main_view.print_no_round_error(tournament.name)
                else:
                    main_view.print_tournament_matches_headline(tournament.name)
                    for round in tournament.rounds:
                        for match in round.matches:
                            print(match)
