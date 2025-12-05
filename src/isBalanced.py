def isShipBalanced(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    mid = cols // 2

    containers = []
    for r in range(rows):
        for c in range(cols):
            cell = grid[r][c]
            if isinstance(cell, int):
                containers.append((cell, r, c))

    count = len(containers)

    # Zero or one container → balanced
    if count <= 1:
        return True, 0, 0

    port = 0
    star = 0
    total = 0

    for w, r, c in containers:
        total += w
        if c < mid:
            port += w
        else:
            star += w

    # Two containers → special case: balanced if they are on opposite sides
    if count == 2:
        _, _, c1 = containers[0]
        _, _, c2 = containers[1]
        onOppSides = (c1 < mid and c2 >= mid) or (c2 < mid and c1 >= mid)
        return onOppSides, port, star

    # Normal rule for 3+ containers
    diff = abs(port - star)
    allowed = total * 0.10

    return diff <= allowed, port, star