import re
import os

ROWS = 8
COLS = 12

def writeOutboundManifest(filename, lines, finalGrid, contentsMap, originalGrid):
    filename = os.path.basename(filename)

    outFolder = os.path.join(os.path.dirname(__file__), "..", "solutions")
    outFolder = os.path.abspath(outFolder)
    os.makedirs(outFolder, exist_ok=True)

    nameNoExt = filename.replace(".txt", "")
    outName = os.path.join(outFolder, nameNoExt + "OUTBOUND.txt")

    containerIdentity = {}
    pattern = r"\[(\d+),(\d+)\],\s*\{(\d+)\},\s*(.*)"
    
    for line in lines:
        match = re.match(pattern, line.strip())
        if match:
            r = int(match.group(1))
            c = int(match.group(2))
            w = int(match.group(3))
            content = match.group(4).strip()
            
            if content not in ("NAN", "UNUSED") and w > 0:
                containerIdentity[(r, c, w)] = content
    
    finalToDesc = {}
    usedContainers = set()
    
    for rFinal in range(ROWS):
        for cFinal in range(COLS):
            val = finalGrid[rFinal][cFinal]
            if isinstance(val, int):
                for (rOrig, cOrig, w), desc in containerIdentity.items():
                    if w == val and (rOrig, cOrig, w) not in usedContainers:
                        finalToDesc[(rFinal, cFinal)] = desc
                        usedContainers.add((rOrig, cOrig, w))
                        break

    output = []
    index = 0

    for line in lines:
        if re.match(r"\[\d{2},\d{2}\]", line):
            r = index // COLS + 1
            c = index % COLS + 1
            rIdx, cIdx = r - 1, c - 1

            val = finalGrid[rIdx][cIdx]

            if val == "NAN":
                weightStr = "00000"
                english = "NAN"
            elif val == "UNUSED":
                weightStr = "00000"
                english = "UNUSED"
            elif isinstance(val, int):
                weightStr = f"{val:05d}"
                english = finalToDesc.get((rIdx, cIdx), "UNKNOWN")
            else:
                weightStr = "00000"
                english = "UNUSED"

            output.append(f"[{r:02d},{c:02d}], {{{weightStr}}}, {english}\n")
            index += 1

        else:
            output.append(line)

    with open(outName, "w") as f:
        f.writelines(output)