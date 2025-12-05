import re
import os

ROWS = 8
COLS = 12

def writeOutboundManifest(filename, lines, finalGrid, contentsMap, originalGrid):
    filename = os.path.basename(filename)

    outFolder = os.path.join(os.path.dirname(__file__), "..", "solutions")
    outFolder = os.path.abspath(outFolder)
    os.makedirs(outFolder, exist_ok=True)

    name_no_ext = filename.replace(".txt", "")
    outName = os.path.join(outFolder, name_no_ext + "OUTBOUND.txt")

    container_identity = {}
    pattern = r"\[(\d+),(\d+)\],\s*\{(\d+)\},\s*(.*)"
    
    for line in lines:
        match = re.match(pattern, line.strip())
        if match:
            r = int(match.group(1))
            c = int(match.group(2))
            w = int(match.group(3))
            content = match.group(4).strip()
            
            if content not in ("NAN", "UNUSED") and w > 0:
                container_identity[(r, c, w)] = content
    
    final_to_desc = {}
    used_containers = set()
    
    for r_final in range(ROWS):
        for c_final in range(COLS):
            val = finalGrid[r_final][c_final]
            if isinstance(val, int):
                for (r_orig, c_orig, w), desc in container_identity.items():
                    if w == val and (r_orig, c_orig, w) not in used_containers:
                        final_to_desc[(r_final, c_final)] = desc
                        used_containers.add((r_orig, c_orig, w))
                        break

    output = []
    index = 0

    for line in lines:
        if re.match(r"\[\d{2},\d{2}\]", line):
            r = index // COLS + 1
            c = index % COLS + 1
            r_idx, c_idx = r - 1, c - 1

            val = finalGrid[r_idx][c_idx]

            if val == "NAN":
                weightStr = "00000"
                english = "NAN"
            elif val == "UNUSED":
                weightStr = "00000"
                english = "UNUSED"
            elif isinstance(val, int):
                weightStr = f"{val:05d}"
                english = final_to_desc.get((r_idx, c_idx), "UNKNOWN")
            else:
                weightStr = "00000"
                english = "UNUSED"

            output.append(f"[{r:02d},{c:02d}], {{{weightStr}}}, {english}\n")
            index += 1

        else:
            output.append(line)

    with open(outName, "w") as f:
        f.writelines(output)