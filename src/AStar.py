import heapq
from copy import deepcopy
import itertools

ROWS = 8
COLS = 12

# Unique tiebreaker counter so heap never compares layouts/keys
counter = itertools.count()


def grid_to_key(grid):
    return tuple(tuple(row) for row in grid)


def compute_imbalance(grid, balance_func):
    balanced, port, star = balance_func(grid)
    return abs(port - star)


def AStar(start_grid, slot_exists, containers, balance_func):
    """
    A* search to find a sequence of moves that produces
    a legally balanced ship.

    start_grid: 8x12 grid containing ints, "UNUSED", "NAN"
    slot_exists: 8x12 boolean matrix
    containers: list of dicts: {"pos": (r,c), "weight": w, "description": txt}
    balance_func: your isBalanced function
    """

    # Heaviest container for heuristic scaling
    max_weight = max(c["weight"] for c in containers) if containers else 1

    start_key = grid_to_key(start_grid)
    start_imb = compute_imbalance(start_grid, balance_func)

    # Heap record format:
    # (f, counterID, g, key, grid, path)
    open_set = []
    heapq.heappush(open_set, (start_imb, next(counter), 0, start_key, start_grid, []))

    visited = {start_key: 0}

    while open_set:
        f, _, g, key, layout, path = heapq.heappop(open_set)

        # Goal check
        balanced, _, _ = balance_func(layout)
        if balanced:
            return path, layout

        # Expand all possible moves
        for r1 in range(ROWS):
            for c1 in range(COLS):
                if not slot_exists[r1][c1]:
                    continue

                cell = layout[r1][c1]
                if not isinstance(cell, int):
                    continue  # Not a container

                container_weight = cell

                # Try moving this container to every UNUSED valid slot
                for r2 in range(ROWS):
                    for c2 in range(COLS):
                        if not slot_exists[r2][c2]:
                            continue
                        if layout[r2][c2] != "UNUSED":
                            continue
                        if (r1 == r2 and c1 == c2):
                            continue

                        # Movement cost
                        move_cost = abs(r1 - r2) + abs(c1 - c2)
                        new_g = g + move_cost

                        # Apply move
                        new_grid = deepcopy(layout)
                        new_grid[r1][c1] = "UNUSED"
                        new_grid[r2][c2] = container_weight

                        new_key = grid_to_key(new_grid)

                        # Seen cheaper before? Skip.
                        if new_key in visited and visited[new_key] <= new_g:
                            continue
                        visited[new_key] = new_g

                        # Heuristic: imbalance left divided by max weight
                        new_imb = compute_imbalance(new_grid, balance_func)
                        h = new_imb / max_weight

                        new_f = new_g + h
                        new_path = path + [((r1, c1), (r2, c2))]

                        heapq.heappush(
                            open_set,
                            (new_f, next(counter), new_g, new_key, new_grid, new_path)
                        )

    return None, None  # no solution
