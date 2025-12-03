
ROWS = 8
COLS = 12

# CURRENTLY WOKRING ON VISMOVE
def visMove(grid, src=None, dst=None, crane_pos=None, highlight_moving=False, highlight_destination=False):
 

    # ANSI color codes
    RESET = "\033[0m"
    BLACK = "\033[40m"    # unused / NaN
    YELLOW = "\033[43m"   # other containers
    GREEN = "\033[42m"    # moving container
    RED = "\033[41m"      # destination
    BLUE = "\033[44m"     # optional: crane position
    WHITE = "\033[47m"

    ROWS = len(grid)
    COLS = len(grid[0])

    # Header
    header = "   " + " ".join(f"{c+1:>3}" for c in range(COLS))
    print("\nShip Layout:\n")
    print(header)
    print("    " + "-" * (COLS * 4 - 1))

    # Flip Y-axis: row 8 on top
    for r in reversed(range(ROWS)):
        row_display = f"{r+1:>2} |"
        for c in range(COLS):
            cell = grid[r][c]

            color = YELLOW  # default: container
            if cell == "UNUSED" or cell is None:
                color = WHITE
            if cell == "NAN":
                color = BLACK
            if highlight_moving and src == (r, c):
                color = GREEN
            if highlight_destination and dst == (r, c):
                color = RED
            if crane_pos == (r, c):
                color = BLUE

            # Display first 3 chars or blank
            content = "   " if cell in ["UNUSED", None] else f"{str(cell)[:3]:>3}"
            row_display += f"{color}{content}{RESET} "
        print(row_display)
    print("\n")  # extra newline for spacing


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
                # Real container weight
                formatted.append(f"{cell:03d}")
            else:
                # Should not occur unless parser is wrong
                formatted.append("??")

            # Add center divider after column 6 (index 5)
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