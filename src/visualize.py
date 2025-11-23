# TO HELP SEE THE GRAPH AS WE ARE WORKING

ROWS = 8
COLS = 12

def visualize_grid(grid):
    print("\nShip Layout:\n")
    
    header = "      " + "  ".join(f"{c:02d}" for c in range(1, COLS + 1))
    print(header)
    print("      " + "-" * (COLS * 4))

    for row in range(ROWS, 0, -1):
        row_display = [grid[row - 1][col] for col in range(COLS)]
        formatted = []

        for col, cell in enumerate(row_display):
            if cell == "NAN":
                formatted.append("XX")
            elif cell == "UNUSED":
                formatted.append("..")
            else:
                weight = cell[0]
                formatted.append(f"{weight:02d}")
            
            # Middle Line
            if col == COLS // 2 - 1:
                formatted.append("|")

        print(f"Row {row:02d} | " + "  ".join(formatted))

    print()
