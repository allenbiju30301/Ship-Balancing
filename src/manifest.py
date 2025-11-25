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

        # Store the English text EXACTLY as in original manifest
        contentsMap[pos] = content

        # Slot physically does NOT exist
        if content == "NAN":
            grid[r-1][c-1] = "NAN"
            slotExists[pos] = False
            continue

        # Slot exists but is empty
        if content == "UNUSED":
            grid[r-1][c-1] = "UNUSED"
            slotExists[pos] = True
            continue

        # REAL container
        grid[r-1][c-1] = w
        slotExists[pos] = True

        containers.append({
            "pos": pos,
            "weight": w,
            "description": content
        })

    return grid, slotExists, containers, contentsMap


def writeOutboundManifest(filename, lines, finalGrid, contentsMap):
    # ensure filename is JUST the name, not full path
    filename = os.path.basename(filename)

    # create /solutions directory (relative to this file's folder)
    outFolder = os.path.join(os.path.dirname(__file__), "..", "solutions")
    outFolder = os.path.abspath(outFolder)
    os.makedirs(outFolder, exist_ok=True)

    # build final outbound file path
    name_no_ext = filename.replace(".txt", "")
    outName = os.path.join(outFolder, name_no_ext + "_OUTBOUND.txt")

    output = []
    index = 0

    for line in lines:
        # match coordinate lines only
        if re.match(r"\[\d{2},\d{2}\]", line):

            r = index // COLS + 1
            c = index % COLS + 1

            val = finalGrid[r-1][c-1]

            # weight formatting
            if val in ("NAN", "UNUSED"):
                weightStr = "00000"
            else:
                weightStr = f"{val:05d}"

            english = contentsMap[(r, c)]

            output.append(f"[{r:02d},{c:02d}], {{{weightStr}}}, {english}\n")
            index += 1

        else:
            # copy comments or header lines unchanged
            output.append(line)

    with open(outName, "w") as f:
        f.writelines(output)
















# import re, os

# ROWS = 8
# COLS = 12

# def parseManifest(lines):
#     grid = [[None] * COLS for _ in range(ROWS)]
#     containers = []
#     slotExists = {}
#     contentsMap = {}   # map (row,col) -> English text

#     pattern = r"\[(\d+),(\d+)\],\s*\{(\d+)\},\s*(.*)"

#     for line in lines:
#         match = re.match(pattern, line.strip())
#         if not match:
#             continue

#         r = int(match.group(1))
#         c = int(match.group(2))
#         w = int(match.group(3))
#         content = match.group(4).strip()

#         pos = (r, c)
#         contentsMap[pos] = content   # always store text

#         if content == "NAN":
#             grid[r-1][c-1] = "NAN"
#             slotExists[pos] = False
#             continue

#         if content == "UNUSED":
#             grid[r-1][c-1] = "UNUSED"
#             slotExists[pos] = True
#             continue

#         # Real container
#         grid[r-1][c-1] = w
#         slotExists[pos] = True

#         containers.append({
#             "pos": pos,
#             "weight": w,
#             "description": content
#         })

#     return grid, slotExists, containers, contentsMap


# def writeOutboundManifest(filename, lines, finalGrid, contentsMap):
#     # Ensure the solutions folder exists one level up
#     solutionsFolder = "../solutions"
#     os.makedirs(solutionsFolder, exist_ok=True)
    
#     outName = os.path.join(solutionsFolder, filename + "_OUTBOUND.txt")
#     output = []

#     index = 0
#     for line in lines:
#         # Match coordinate lines
#         if re.match(r"\[\d{2},\d{2}\]", line):

#             r = index // COLS + 1
#             c = index % COLS + 1

#             val = finalGrid[r-1][c-1]

#             # Weight formatting
#             if val in ("NAN", "UNUSED"):
#                 weightStr = "00000"
#             else:
#                 weightStr = f"{val:05d}"

#             english = contentsMap[(r, c)]
#             newLine = f"[{r:02d},{c:02d}], {{{weightStr}}}, {english}\n"
#             output.append(newLine)
#             index += 1
#         else:
#             output.append(line)

#     with open(outName, "w") as f:
#         f.writelines(output)

#     print(f"\nWrote outbound manifest: {outName}")