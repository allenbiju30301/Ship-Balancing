import re
import os

ROWS = 8
COLS = 12

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

    # Build a reverse map: weight -> description
    weight_to_description = {}
    for (r, c), desc in contentsMap.items():
        # Get original weight at this position from the map
        # We need to scan the original lines to build this
        pass
    
    # Actually, we need to get descriptions from the original grid
    # Let's build weight->description from contentsMap by parsing lines
    weight_to_desc = {}
    temp_index = 0
    pattern = r"\[(\d+),(\d+)\],\s*\{(\d+)\},\s*(.*)"
    for line in lines:
        match = re.match(pattern, line.strip())
        if match:
            r = int(match.group(1))
            c = int(match.group(2))
            w = int(match.group(3))
            content = match.group(4).strip()
            
            # If this had a real container (not NAN/UNUSED), map weight to description
            if content not in ("NAN", "UNUSED") and w > 0:
                weight_to_desc[w] = content

    output = []
    index = 0

    for line in lines:
        # match coordinate lines only
        if re.match(r"\[\d{2},\d{2}\]", line):
            r = index // COLS + 1
            c = index % COLS + 1

            val = finalGrid[r-1][c-1]

            # weight formatting and description
            if val == "NAN":
                weightStr = "00000"
                english = "NAN"
            elif val == "UNUSED":
                weightStr = "00000"
                english = "UNUSED"
            elif isinstance(val, int):
                # Real container - get description from weight
                weightStr = f"{val:05d}"
                english = weight_to_desc.get(val, "UNKNOWN")
            else:
                weightStr = "00000"
                english = "UNUSED"

            output.append(f"[{r:02d},{c:02d}], {{{weightStr}}}, {english}\n")
            index += 1

        else:
            # copy comments or header lines unchanged
            output.append(line)

    with open(outName, "w") as f:
        f.writelines(output)