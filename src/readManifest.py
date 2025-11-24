import re

ROWS = 8
COLS = 12

def parse_manifest(lines):
    grid = [[None] * COLS for _ in range(ROWS)]
    containers = []
    slot_exists = {}
    contents_map = {}   # NEW: map (row,col) -> english text

    pattern = r"\[(\d+),(\d+)\],\s*\{(\d+)\},\s*(.*)"

    for line in lines:
        match = re.match(pattern, line.strip())
        if not match:
            continue

        r = int(match.group(1))
        c = int(match.group(2))
        w = int(match.group(3))
        content = match.group(4).strip()

        pos = (r, c)
        contents_map[pos] = content   # ALWAYS store English text

        # NAN slot = physically nonexistent
        if content == "NAN":
            grid[r-1][c-1] = "NAN"
            slot_exists[pos] = False
            continue

        # UNUSED slot = exists, empty
        if content == "UNUSED":
            grid[r-1][c-1] = "UNUSED"
            slot_exists[pos] = True
            continue

        # Real container
        grid[r-1][c-1] = w
        slot_exists[pos] = True

        containers.append({
            "pos": pos,
            "weight": w,
            "description": content
        })

    return grid, slot_exists, containers, contents_map