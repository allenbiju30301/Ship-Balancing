import heapq
from copy import deepcopy
import itertools

ROWS = 8
COLS = 12
_counter = itertools.count()

def buildSlotMatrix(slotExistsDict):
    matrix = [[False] * COLS for _ in range(ROWS)]
    for r in range(ROWS):
        for c in range(COLS):
            matrix[r][c] = slotExistsDict.get((r + 1, c + 1), False)
    return matrix

def gridKey(grid):
    return tuple(tuple(row) for row in grid)

def imbalance(grid, balanceFunc):
    _, port, star = balanceFunc(grid)
    return abs(port - star)

def supported(grid, r, c):
    if r == 0:
        return True
    below = grid[r - 1][c]
    return isinstance(below, int)

def topOfStack(grid, r, c):
    for rr in range(r + 1, ROWS):
        if isinstance(grid[rr][c], int):
            return False
    return True

def manhattan(a, b):
    (r1, c1) = a
    (r2, c2) = b
    return abs(r1 - r2) + abs(c1 - c2)

def aStar(grid, slotMatrix, containers, balanceFunc, craneStart=(0, 7)):
    if not containers:
        return [], grid

    maxW = max(c["weight"] for c in containers)
    startKey = gridKey(grid)

    openSet = []
    startF = imbalance(grid, balanceFunc)
    heapq.heappush(openSet, (startF, next(_counter), 0, grid, [], craneStart))
    visited = {(startKey, craneStart): 0}

    while openSet:
        f, _, g, layout, path, cranePos = heapq.heappop(openSet)

        balanced, _, _ = balanceFunc(layout)
        if balanced:
            return path, layout

        for r1 in range(ROWS):
            for c1 in range(COLS):
                if not slotMatrix[r1][c1]:
                    continue
                if not isinstance(layout[r1][c1], int):
                    continue
                if not topOfStack(layout, r1, c1):
                    continue

                w = layout[r1][c1]

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

                        moveCost = manhattan(cranePos, (r1, c1)) + manhattan((r1, c1), (r2, c2))
                        newG = g + moveCost

                        newGrid = deepcopy(layout)
                        newGrid[r1][c1] = "UNUSED"
                        newGrid[r2][c2] = w

                        key = gridKey(newGrid)
                        stateKey = (key, (r2, c2))
                        if stateKey in visited and visited[stateKey] <= newG:
                            continue
                        visited[stateKey] = newG

                        h = imbalance(newGrid, balanceFunc) / maxW if maxW > 0 else 0
                        newF = newG + h
                        newPath = path + [((r1, c1), (r2, c2))]

                        heapq.heappush(openSet, (newF, next(_counter), newG, newGrid, newPath, (r2, c2)))

    return None, None