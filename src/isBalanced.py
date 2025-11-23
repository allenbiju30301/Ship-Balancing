def isShipBalanced(grid):
    ROWS = len(grid)
    COLS = len(grid[0]) if ROWS > 0 else 0
    
    if ROWS == 0 or COLS == 0:
        return True, 0, 0  # empty ship is balanced

    portWeight = 0
    starboardWeight = 0
    totalWeight = 0
    mid = COLS // 2  # columns 0-5 = port, 6-11 = starboard

    for r in range(ROWS):
        for c in range(COLS):
            cell = grid[r][c]

            if isinstance(cell, int):  # REAL CONTAINER
                w = cell
                totalWeight += w

                if c < mid:
                    portWeight += w
                else:
                    starboardWeight += w

            # ignore "UNUSED" and "NAN"

    difference = abs(portWeight - starboardWeight)
    allowedDiff = totalWeight * 0.10

    balanced = (difference == 0) or (difference <= allowedDiff)

    return balanced, portWeight, starboardWeight