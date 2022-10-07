from models.player import Player
from models.match import Match
from models.round import Round
from models.tournament import Tournament


roman = Player("Roman", "Saint-hilaire", 10, 6, 1993, "M")
delil = Player("Delil", "Dogan", 10, 6, 1992, "M")

nicolas = Player("Nicolas", "Saint-hilaire", 19, 9, 1994, "M")
loic = Player("Loic", "Saint-hilaire", 31, 8, 1991, "M")

match_1 = Match(roman, 2, delil, 5)
match_2 = Match(nicolas, 2, loic, 3)

round = Round("Round 1", [match_1, match_2])

round.save()

pouet = 1
for a in range(30000000):
    pouet += 1

round.finish()

tournament = Tournament("Tournoi test", "Description test", "Montpellier", "Bullet", 8, 10, 2023)

tournament.add_player(roman)
tournament.add_player(delil)
tournament.add_player(loic)
tournament.add_player(nicolas)

tournament.add_round(round)

tournament.save()

print(tournament)
