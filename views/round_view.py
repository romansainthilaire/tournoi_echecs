from tinydb.table import Table


class RoundView:
    """Gets round information from the user or shows round information to the user."""

    def __init__(self, rounds_table: Table):
        self.rounds_table: Table = rounds_table
