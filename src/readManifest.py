import re
import os

ROWS = 8
COLS = 12

def parseManifest(lines):
    grid = [[None] * COLS for _ in range(ROWS)]
    containers = []
    slotExists = {}
    contentsMap = {}

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
        contentsMap[pos] = content

        # Unavailable slot
        if content == "NAN":
            grid[r-1][c-1] = "NAN"
            slotExists[pos] = False
            continue

        # Available but empty
        if content == "UNUSED":
            grid[r-1][c-1] = "UNUSED"
            slotExists[pos] = True
            continue

        # Actual container
        grid[r-1][c-1] = w
        slotExists[pos] = True

        containers.append({
            "pos": pos,
            "weight": w,
            "description": content
        })

    return grid, slotExists, containers, contentsMap