import re
import os

ROWS = 8
COLS = 12

def writeOutboundManifest(filename, lines, finalGrid, contentsMap, originalGrid):
    """
    Write outbound manifest with containers in their new positions.
    
    Args:
        filename: Name of the manifest file
        lines: Original manifest file lines
        finalGrid: Grid after balancing moves
        contentsMap: Original (position -> description) mapping
        originalGrid: Original grid state before moves
    """
    # ensure filename is JUST the name, not full path
    filename = os.path.basename(filename)

    # create /solutions directory (relative to this file's folder)
    outFolder = os.path.join(os.path.dirname(__file__), "..", "solutions")
    outFolder = os.path.abspath(outFolder)
    os.makedirs(outFolder, exist_ok=True)

    # build final outbound file path
    name_no_ext = filename.replace(".txt", "")
    outName = os.path.join(outFolder, name_no_ext + "_OUTBOUND.txt")

    # Build mapping: (original_row, original_col, weight) -> description
    # This uniquely identifies each container even with duplicate weights
    container_identity = {}
    pattern = r"\[(\d+),(\d+)\],\s*\{(\d+)\},\s*(.*)"
    
    for line in lines:
        match = re.match(pattern, line.strip())
        if match:
            r = int(match.group(1))
            c = int(match.group(2))
            w = int(match.group(3))
            content = match.group(4).strip()
            
            # Map (position, weight) to description for unique identification
            if content not in ("NAN", "UNUSED") and w > 0:
                container_identity[(r, c, w)] = content
    
    # Build reverse mapping for finalGrid: each position -> description
    # Match weights in finalGrid to their original descriptions
    final_to_desc = {}
    used_containers = set()  # Track which original containers we've assigned
    
    for r_final in range(ROWS):
        for c_final in range(COLS):
            val = finalGrid[r_final][c_final]
            if isinstance(val, int):
                # Find an unused container with this weight from original grid
                for (r_orig, c_orig, w), desc in container_identity.items():
                    if w == val and (r_orig, c_orig, w) not in used_containers:
                        final_to_desc[(r_final, c_final)] = desc
                        used_containers.add((r_orig, c_orig, w))
                        break

    output = []
    index = 0

    for line in lines:
        # match coordinate lines only
        if re.match(r"\[\d{2},\d{2}\]", line):
            r = index // COLS + 1
            c = index % COLS + 1
            r_idx, c_idx = r - 1, c - 1

            val = finalGrid[r_idx][c_idx]

            # weight formatting and description
            if val == "NAN":
                weightStr = "00000"
                english = "NAN"
            elif val == "UNUSED":
                weightStr = "00000"
                english = "UNUSED"
            elif isinstance(val, int):
                # Real container - get description from mapping
                weightStr = f"{val:05d}"
                english = final_to_desc.get((r_idx, c_idx), "UNKNOWN")
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