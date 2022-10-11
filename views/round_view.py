from tinydb.table import Table


class RoundView:

    def __init__(self, rounds_table: Table):
        self.rounds_table = rounds_table
