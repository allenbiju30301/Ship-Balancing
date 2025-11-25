import heapq
from copy import deepcopy
from collections import deque
import itertools

ROWS = 8
COLS = 12
counter = itertools.count()

def buildSlotMatrix(slotExistsDict):
    matrix = [[False] * COLS for _ in range(ROWS)]
    for r in range(ROWS):
        for c in range(COLS):
            matrix[r][c] = slotExistsDict.get((r + 1, c + 1), False)
    return matrix

def gridKey(grid):
    return tuple(tuple(row) for row in grid)

def imbalance(grid, balanceFunc):
    b, p, s = balanceFunc(grid)
    return abs(p - s)

def supported(grid, r, c):
    if r == 0:
        return True
    return isinstance(grid[r - 1][c], int)

def topOfStack(grid, r, c):
    for rr in range(r + 1, ROWS):
        if isinstance(grid[rr][c], int):
            return False
    return True

def bfs(start, goal, grid, ignoreContainers):
    q = deque([(start, 0)])
    seen = {start}

    while q:
        (r, c), d = q.popleft()
        if (r, c) == goal:
            return d

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < ROWS and 0 <= nc < COLS):
                continue
            if (nr, nc) in seen:
                continue

            cell = grid[nr][nc]

            if ignoreContainers:
                if cell != "NAN":
                    seen.add((nr, nc))
                    q.append(((nr, nc), d + 1))
            else:
                if cell == "UNUSED" or cell == "NAN":
                    seen.add((nr, nc))
                    q.append(((nr, nc), d + 1))

    return None

def aStar(grid, slotMatrix, containers, balanceFunc, craneStart=(0, 7)):
    # No containers or 1 container → no moves needed
    if len(containers) <= 1:
        return [], grid

    # Special case: 2 containers must be on opposite sides
    if len(containers) == 2:
        (_, r1, c1) = containers[0]["weight"], containers[0]["pos"][0] - 1, containers[0]["pos"][1] - 1
        (_, r2, c2) = containers[1]["weight"], containers[1]["pos"][0] - 1, containers[1]["pos"][1] - 1
        mid = COLS // 2
        opposite = (c1 < mid and c2 >= mid) or (c2 < mid and c1 >= mid)
        if opposite:
            return [], grid  # Already balanced enough not to move

    maxW = max(c["weight"] for c in containers)
    startKey = gridKey(grid)

    openSet = []
    heapq.heappush(openSet, (imbalance(grid, balanceFunc), next(counter), 0, grid, [], craneStart))
    visited = {(startKey, craneStart): 0}

    while openSet:
        f, _, g, layout, path, cranePos = heapq.heappop(openSet)

        balanced, _, _ = balanceFunc(layout)
        if balanced:
            return path, layout

        # Try every container as a source
        for r1 in range(ROWS):
            for c1 in range(COLS):
                if not slotMatrix[r1][c1]:
                    continue
                if not isinstance(layout[r1][c1], int):
                    continue
                if not topOfStack(layout, r1, c1):
                    continue

                w = layout[r1][c1]

                # Try every empty cell as a destination
                for r2 in range(ROWS):
                    for c2 in range(COLS):
                        if not slotMatrix[r2][c2]:
                            continue
                        if layout[r2][c2] != "UNUSED":
                            continue
                        if (r1, c1) == (r2, c2):
                            continue
                        if not supported(layout, r2, c2):
                            continue

                        dist1 = bfs(cranePos, (r1, c1), layout, True)
                        if dist1 is None:
                            continue

                        dist2 = bfs((r1, c1), (r2, c2), layout, False)
                        if dist2 is None:
                            continue

                        newG = g + dist1 + dist2
                        newGrid = deepcopy(layout)

                        newGrid[r1][c1] = "UNUSED"
                        newGrid[r2][c2] = w

                        newKey = gridKey(newGrid)
                        stateKey = (newKey, (r2, c2))

                        if stateKey in visited and visited[stateKey] <= newG:
                            continue
                        visited[stateKey] = newG

                        h = imbalance(newGrid, balanceFunc) / maxW
                        newF = newG + h
                        newPath = path + [((r1, c1), (r2, c2))]

                        heapq.heappush(
                            openSet,
                            (newF, next(counter), newG, newGrid, newPath, (r2, c2))
                        )

    return None, None













# import heapq
# from copy import deepcopy
# import itertools

# ROWS = 8
# COLS = 12
# _counter = itertools.count()

# def buildSlotMatrix(slotExistsDict):
#     matrix = [[False] * COLS for _ in range(ROWS)]
#     for r in range(ROWS):
#         for c in range(COLS):
#             matrix[r][c] = slotExistsDict.get((r + 1, c + 1), False)
#     return matrix

# def gridKey(grid):
#     return tuple(tuple(row) for row in grid)

# def imbalance(grid, balanceFunc):
#     _, port, star = balanceFunc(grid)
#     return abs(port - star)

# def supported(grid, r, c):
#     if r == 0:
#         return True
#     below = grid[r - 1][c]
#     return isinstance(below, int)

# def topOfStack(grid, r, c):
#     for rr in range(r + 1, ROWS):
#         if isinstance(grid[rr][c], int):
#             return False
#     return True

# def manhattan(a, b):
#     (r1, c1) = a
#     (r2, c2) = b
#     return abs(r1 - r2) + abs(c1 - c2)

# def aStar(grid, slotMatrix, containers, balanceFunc, craneStart=(0, 7)):
#     if not containers:
#         return [], grid

#     maxW = max(c["weight"] for c in containers)
#     startKey = gridKey(grid)

#     openSet = []
#     startF = imbalance(grid, balanceFunc)
#     heapq.heappush(openSet, (startF, next(_counter), 0, grid, [], craneStart))
#     visited = {(startKey, craneStart): 0}

#     while openSet:
#         f, _, g, layout, path, cranePos = heapq.heappop(openSet)

#         balanced, _, _ = balanceFunc(layout)
#         if balanced:
#             return path, layout

#         for r1 in range(ROWS):
#             for c1 in range(COLS):
#                 if not slotMatrix[r1][c1]:
#                     continue
#                 if not isinstance(layout[r1][c1], int):
#                     continue
#                 if not topOfStack(layout, r1, c1):
#                     continue

#                 w = layout[r1][c1]

#                 for r2 in range(ROWS):
#                     for c2 in range(COLS):
#                         if not slotMatrix[r2][c2]:
#                             continue
#                         if layout[r2][c2] != "UNUSED":
#                             continue
#                         if (r1, c1) == (r2, c2):
#                             continue
#                         if not supported(layout, r2, c2):
#                             continue

#                         moveCost = manhattan(cranePos, (r1, c1)) + manhattan((r1, c1), (r2, c2))
#                         newG = g + moveCost

#                         newGrid = deepcopy(layout)
#                         newGrid[r1][c1] = "UNUSED"
#                         newGrid[r2][c2] = w

#                         key = gridKey(newGrid)
#                         stateKey = (key, (r2, c2))
#                         if stateKey in visited and visited[stateKey] <= newG:
#                             continue
#                         visited[stateKey] = newG

#                         h = imbalance(newGrid, balanceFunc) / maxW if maxW > 0 else 0
#                         newF = newG + h
#                         newPath = path + [((r1, c1), (r2, c2))]

#                         heapq.heappush(openSet, (newF, next(_counter), newG, newGrid, newPath, (r2, c2)))

#     return None, None