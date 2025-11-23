import re

ROWS = 8
COLS = 12

def parse_manifest(lines):
    grid = [[None] * COLS for _ in range(ROWS)]
    containers = []
    slot_exists = {}

    pattern = r"\[(\d+),(\d+)\],\s*\{(\d+)\},\s*(.*)"

    for line in lines:
        match = re.match(pattern, line.strip())
        if not match:
            continue

        r, c, w, content = int(match.group(1)), int(match.group(2)), int(match.group(3)), match.group(4).strip()
        pos = (r, c)

        if content in ("NAN", "UNUSED"):
            grid[r-1][c-1] = content
            slot_exists[pos] = content != "NAN"
        else:
            grid[r-1][c-1] = (w, content)
            slot_exists[pos] = True
            containers.append({"pos": pos, "weight": w, "description": content})

    return grid, slot_exists, containers
