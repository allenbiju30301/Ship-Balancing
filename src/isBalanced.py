def isShipBalanced(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    if rows == 0 or cols == 0:
        return True, 0, 0

    mid = cols // 2  # 0..mid-1 port, mid..cols-1 star

    containers = []
    for r in range(rows):
        for c in range(cols):
            cell = grid[r][c]
            if isinstance(cell, int):
                containers.append((cell, r, c))

    count = len(containers)

    # 0 or 1 container: always balanced
    if count <= 1:
        return True, 0, 0

    # Compute port / star weights for all containers
    port = 0
    star = 0
    total = 0
    for w, r, c in containers:
        total += w
        if c < mid:
            port += w
        else:
            star += w

    # Exactly 2 containers → special case "opposite sides is enough"
    if count == 2:
        _, _, c1 = containers[0]
        _, _, c2 = containers[1]
        onOppSides = (c1 < mid and c2 >= mid) or (c2 < mid and c1 >= mid)
        return onOppSides, port, star

    # 3+ containers → 10% rule
    diff = abs(port - star)
    allowed = total * 0.10
    balanced = (diff == 0) or (diff <= allowed)
    return balanced, port, star