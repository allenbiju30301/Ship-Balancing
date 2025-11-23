def is_ship_balanced(grid):
    ROWS = len(grid)
    COLS = len(grid[0]) if ROWS > 0 else 0
    
    if ROWS == 0 or COLS == 0:
        return True, 0, 0  # empty ship is balanced

    port_weight = 0
    starboard_weight = 0
    total_weight = 0
    mid = COLS // 2  # columns 0-5 = port, 6-11 = starboard

    for r in range(ROWS):
        for c in range(COLS):
            cell = grid[r][c]

            if isinstance(cell, int):  # REAL CONTAINER
                w = cell
                total_weight += w

                if c < mid:
                    port_weight += w
                else:
                    starboard_weight += w

            # ignore "UNUSED" and "NAN"

    difference = abs(port_weight - starboard_weight)
    allowed_diff = total_weight * 0.10

    balanced = (difference == 0) or (difference <= allowed_diff)

    return balanced, port_weight, starboard_weight









# def is_ship_balanced(grid):
#     ROWS = len(grid)
#     COLS = len(grid[0]) if ROWS > 0 else 0
    
#     if ROWS == 0 or COLS == 0:
#         return True  # empty ship is balanced

#     port_weight = 0
#     starboard_weight = 0
#     total_weight = 0
#     mid = COLS // 2

#     for r in range(ROWS):
#         for c in range(COLS):
#             cell = grid[r][c]
#             if isinstance(cell, tuple):  # (weight, content)
#                 w = cell[0]
#                 total_weight += w
#                 if c < mid:
#                     port_weight += w
#                 else:
#                     starboard_weight += w

#     # legal balance: difference <= 10% of total weight
#     difference = abs(port_weight - starboard_weight)
#     allowed_diff = total_weight * 0.10

#     return difference <= allowed_diff, port_weight, starboard_weight
