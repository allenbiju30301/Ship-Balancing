import heapq
from copy import deepcopy
from collections import deque
import itertools

counter = itertools.count()
ROWS = 8
COLS = 12
PARK_POS = (7, 0)  # Park at [08, 01] in display coordinates

def manhattan_distance(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

def buildSlotMatrix(slotExists):
    matrix = [[False for _ in range(COLS)] for _ in range(ROWS)]
    
    for (r, c), exists in slotExists.items():
        # slotExists uses 1-indexed coordinates from manifest
        # Convert to 0-indexed for grid
        r_idx = r - 1
        c_idx = c - 1
        if 0 <= r_idx < ROWS and 0 <= c_idx < COLS:
            matrix[r_idx][c_idx] = exists
    
    return matrix

def topOfStack(grid, r, c):
    for rr in range(r + 1, ROWS):
        if isinstance(grid[rr][c], int):
            return False
    return True

def supported(grid, r, c):
    if r == 0:
        return True
    return isinstance(grid[r - 1][c], int)

def bfs_distance(grid, start, goal, ignoreContainers=False):
    q = deque([(start, 0)])
    seen = {start}
    while q:
        (r, c), d = q.popleft()
        if (r, c) == goal:
            return d
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            
            # Allow parking position as special case
            if (nr, nc) == PARK_POS:
                if (nr, nc) not in seen:
                    seen.add((nr, nc))
                    q.append(((nr, nc), d+1))
                continue
            
            # Regular grid bounds check
            if 0 <= nr < ROWS and 0 <= nc < COLS and (nr,nc) not in seen:
                cell = grid[nr][nc]
                if ignoreContainers and isinstance(cell, int) and (nr,nc) != goal:
                    continue
                if not ignoreContainers and isinstance(cell, int):
                    continue
                if cell != "UNUSED" and (nr,nc) != goal:
                    continue
                seen.add((nr,nc))
                q.append(((nr,nc), d+1))
    return None

def gridKey(grid):
    return tuple(tuple(row) for row in grid)

def imbalance(grid, balanceFunc):
    b, p, s = balanceFunc(grid)
    return abs(p - s)

def aStar(grid, slotMatrix, containers, balanceFunc, craneStart=PARK_POS):
    if len(containers) <= 1:
        return [], grid

    maxW = max(c["weight"] for c in containers)
    startKey = gridKey(grid)

    openSet = []
    initial_h = imbalance(grid, balanceFunc)
    heapq.heappush(openSet, (initial_h, 0, 0, next(counter), 0, grid, [], craneStart))
    visited = {(startKey, craneStart): 0}

    while openSet:
        f, _, _, _, g, layout, path, cranePos = heapq.heappop(openSet)
        balanced, p, s = balanceFunc(layout)
        
        if balanced:
            return path, layout

        # prioritize containers closer to starboard/destinations
        movable_containers = []
        for r1 in range(ROWS):
            for c1 in range(COLS):
                if not slotMatrix[r1][c1]:
                    continue
                if not isinstance(layout[r1][c1], int):
                    continue
                if not topOfStack(layout, r1, c1):
                    continue
                movable_containers.append((r1, c1))
        
        movable_containers.sort(key=lambda pos: (pos[0], -pos[1]))
        
        for r1, c1 in movable_containers:
            w = layout[r1][c1]

            # Try placing in all available slots
            for r2 in range(ROWS):
                for c2 in range(COLS):
                    if not slotMatrix[r2][c2] or layout[r2][c2] != "UNUSED":
                        continue
                    if (r1, c1) == (r2, c2):
                        continue
                    if not supported(layout, r2, c2):
                        continue

                    dist1 = manhattan_distance(cranePos, (r1, c1))
                    dist2 = manhattan_distance((r1, c1), (r2, c2))

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
                        (newF, r2, c2, next(counter), newG, newGrid, newPath, (r2, c2))
                    )

    return None, None