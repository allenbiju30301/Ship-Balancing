def visualizeGrid(grid):
    pass










# ROWS = 8
# COLS = 12

# def visualizeGrid(grid):
#     print("\nShip Layout:\n")

#     header = "      " + "  ".join(f"{c:02d}" for c in range(1, COLS + 1))
#     print(header)
#     print("      " + "-" * (COLS * 4))

#     for row in range(ROWS, 0, -1):
#         rowDisplay = [grid[row - 1][col] for col in range(COLS)]
#         formatted = []

#         for col, cell in enumerate(rowDisplay):
#             if cell == "NAN":
#                 formatted.append("XX")
#             elif cell == "UNUSED":
#                 formatted.append("..")
#             elif isinstance(cell, int):
#                 # Real container weight
#                 formatted.append(f"{cell:03d}")
#             else:
#                 # Should not occur unless parser is wrong
#                 formatted.append("??")

#             # Add center divider after column 6 (index 5)
#             if col == COLS // 2 - 1:
#                 formatted.append("|")

#         print(f"Row {row:02d} | " + "  ".join(formatted))

#     print()