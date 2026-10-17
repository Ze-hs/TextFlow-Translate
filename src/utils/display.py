import sqlite3

from rich.console import Console
from rich.table import Table

def print_query_results(rows: list[sqlite3.Row]):
    """
    Prints out the results of a sqlite3 row in a nice format
    :param rows:
    :return:
    """
    console = Console()
    if not rows:
        console.print("No results found.")
        return
    table = Table(show_lines=True)

    for column in rows[0].keys():
        table.add_column(
            column,
            max_width=20,
            overflow="ellipsis",
            justify="center",
            no_wrap=True,
        )

    for row in rows:
        values = []

        for value in row:
            # Rich interprets \n as hard line breaks, messing up the no_wrap rules
            # I'm hard coding this cuz im too lazy.
            if value is None:
                values.append("")
                continue

            text = " ".join(str(value).split())
            values.append(text)

        table.add_row(*values)

    console.print(table)