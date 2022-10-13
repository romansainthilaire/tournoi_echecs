from typing import Optional

from tinydb.table import Table


class MatchView:

    def __init__(self, matches_table: Table):
        self.matches_table: Table = matches_table

    def get_winner_id(
        self,
        match_index: int,
        name_player_1: str,
        id_player_1: Optional[int],
        name_player_2: str,
        id_player_2: Optional[int]
    ) -> int:
        print(
            f"\n\tMatch {match_index}"
            f"\n\t · {name_player_1} - ID {id_player_1}"
            f"\n\t · {name_player_2} - ID {id_player_2}\n"
        )
        winner_id = -1
        while winner_id not in [id_player_1, id_player_2, 0]:
            try:
                winner_id = int(input("\tID du vainqueur (0 si égalité) : "))
            except ValueError:
                continue
        return winner_id
