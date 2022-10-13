from pathlib import Path
from typing import List, Optional

from tinydb import TinyDB

from models.player import Player
from models.match import Match
from models.round import Round


db = TinyDB(Path(__file__).parent.parent / "db.json", indent=4)
tournaments_table = db.table("tournaments")


class Tournament():
    """Represents a chess tournament."""

    def __init__(
        self,
        name: str,
        description: str,
        location: str,
        time_control: str,
        date: str
    ):
        """Inits a tournament.

        Arguments:
            name -- name of the tournament
            description -- description of the tournament
            location -- location of the tournament
            time_control -- time control type (bullet, blitz or coup rapide)
            date -- starting date of the tournament (format : DD/MM/YYYY)
        """
        self.id: Optional[int] = None
        self.name: str = name
        self.description: str = description
        self.location: str = location
        self.time_control: str = time_control
        self.date: str = date
        self.total_rounds: int = 4
        self.rounds_completed: int = 0
        self.players: List[Player] = []
        self.rounds: List[Round] = []

    def __str__(self):
        """String representation of a tournament."""
        return (
            f"\nID {self.id}"
            f"\n\t{self.name}"
            f"\n\tDescription : {self.description}"
            f"\n\tLieu : {self.location}"
            f"\n\tContrôle de temps : {self.time_control}"
            f"\n\tDate : {self.date}"
            f"\n\tNombre de joueurs : {len(self.players)}" + "\n"
            f"\tRounds réalisés : {self.rounds_completed}/{self.total_rounds}"
        )

    @property
    def serialized(self):
        """Turns a tournament object into a dictionary.

        Returns:
            A dictionary of the tournament attributes.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "time_control": self.time_control,
            "date": self.date,
            "total_rounds": self.total_rounds,
            "rounds_completed": self.rounds_completed,
            "players": [player.serialized for player in self.players],
            "rounds": [round.serialized for round in self.rounds],
        }

    def save(self):
        """Saves or updates a tournament into a TinyDB database."""
        if self.id is None:
            self.id = tournaments_table.insert(self.serialized)
            tournaments_table.update({"id": self.id}, doc_ids=[self.id])
        else:
            tournaments_table.update(self.serialized, doc_ids=[self.id])
            for player in self.players:
                player.save()
            for round in self.rounds:
                round.save()

    def get_players_sorted_by_ranking(self) -> List[Player]:
        """Sorts the tournament players by Elo ranking.

        Returns:
            The tournament players sorted by Elo ranking.
        """
        return sorted(
            self.players,
            key=lambda player: (-player.ranking, player.name)
        )

    def get_players_sorted_by_points(self) -> List[Player]:
        """Sorts the tournament players by points.

        Returns:
            The tournament players sorted by points.
        """
        return sorted(
            self.players,
            key=lambda player: (player.points, player.ranking),
            reverse=True
        )

    def add_player(self, player: Player):
        """Adds a player to the tournament."""
        self.players.append(player)
        self.save()

    def add_round(self):
        """Adds a round to the tournament."""
        round_name = f"Round {self.rounds_completed + 1}"
        round = Round(round_name)
        self.rounds.append(round)
        self.save()

    def add_matches(self):
        """
        Generates and adds matches to the tournament.

        If it is the first round, matches are generated as follows:
            1. players are sorted by ranking
            2. players are divided in two halves: upper halve and lower halve
            3. the first player of the upper halve is paired with the first
              player of the lower halve
            4. steps 1 to 3 are repeated until all players are paired

        If it isn't the first round, matches are generated as follows:
            1. players are sorted by points
            2. the first player is paired with the second player
            3. if the first player already played with the second player
               the first player is paired with the third player, etc.
            4. steps 1 to 3 are repeated until all players are paired
        """
        current_round = self.rounds[-1]
        if self.rounds_completed == 0:  # first_round
            players = self.get_players_sorted_by_ranking()
            best_players = players[:len(players) // 2]
            worst_players = players[len(players) // 2:]
            for player_1, player_2 in zip(best_players, worst_players):
                player_1.opponent_ids.append(player_2.id)
                player_2.opponent_ids.append(player_1.id)
                match = Match(player_1, player_2)
                match.save()
                current_round.add_match(match)
        else:
            players = self.get_players_sorted_by_points()
            while True:
                player_1 = players.pop(0)
                for player_2 in players:
                    if player_1.id not in player_2.opponent_ids:
                        player_1.opponent_ids.append(player_2.id)
                        player_2.opponent_ids.append(player_1.id)
                        match = Match(player_1, player_2)
                        match.save()
                        current_round.add_match(match)
                        players.remove(player_2)
                        break
                if players == []:
                    break

    def start_round(self):
        """Adds a round and generates matches for this round."""
        self.add_round()
        self.add_matches()
        self.save()

    def finish_round(self):
        """Ends the current round."""
        current_round = self.rounds[-1]
        current_round.finish()
        self.rounds_completed += 1
        self.players = []
        for match in current_round.matches:
            self.players.extend([match.player_1, match.player_2])
        self.save()
        if self.rounds_completed == self.total_rounds:
            for player in self.players:
                player.reset()
