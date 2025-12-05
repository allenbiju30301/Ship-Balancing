ROWS = 8
COLS = 12

def visMove(grid, src=None, dst=None, cranePos=None, highlightMoving=False, highlightDestination=False):
    # Color codes
    RESET = "\033[0m"
    BLACK = "\033[40m"
    YELLOW = "\033[43m"
    GREEN = "\033[42m"
    RED = "\033[41m"
    BLUE = "\033[44m"
    WHITE = "\033[47m"

    rows = len(grid)
    cols = len(grid[0])

    header = "   " + " ".join(f"{c+1:>3}" for c in range(cols))
    print("\nShip Layout:\n")
    print(header)
    print("    " + "-" * (cols * 4 - 1))

    for r in reversed(range(rows)):
        rowDisplay = f"{r+1:>2} |"
        for c in range(cols):
            cell = grid[r][c]

            color = YELLOW
            if cell == "UNUSED" or cell is None:
                color = WHITE
            if cell == "NAN":
                color = BLACK
            if highlightMoving and src == (r, c):
                color = GREEN
            if highlightDestination and dst == (r, c):
                color = RED
            if cranePos == (r, c):
                color = BLUE

            content = "   " if cell in ["UNUSED", None] else f"{str(cell)[:3]:>3}"
            rowDisplay += f"{color}{content}{RESET} "
        print(rowDisplay)
    print("\n")


def visualizeGrid(grid):
    print("\nShip Layout:\n")

    for row in range(ROWS, 0, -1):
        rowDisplay = [grid[row - 1][col] for col in range(COLS)]
        formatted = []

        for col, cell in enumerate(rowDisplay):
            if cell == "NAN":
                formatted.append("XXX")
            elif cell == "UNUSED":
                formatted.append("...")
            elif isinstance(cell, int):
                formatted.append(f"{cell:03d}")
            else:
                formatted.append("??")

            if col == COLS // 2 - 1:
                formatted.append("|")

        print(f"Row {row:02d} | " + "  ".join(formatted))

    header = "         " + "   ".join(
        (f"{c:02d}   " if c == 6 else f"{c:02d}")
        for c in range(1, COLS + 1)
    )
    print(header)
    print("         " + "-" * (COLS * 5))
    print()