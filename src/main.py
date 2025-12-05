import os
from readManifest import parseManifest
from writeManifest import writeOutboundManifest
from isBalanced import isShipBalanced
from AStar import aStar, buildSlotMatrix, manhattanDistance
from visualize import visualizeGrid as vis
from visualize import visMove
from logger import logEvent, logUserComment, saveLog

ROWS = 8
COLS = 12
PARK_POS = (7, 0)  # Park at [08, 01] in display coordinates

def runInstructions(path, grid, slotMatrix, containers, balanceFunc):
    print(f"\n{os.path.basename(path)} has {len(containers)} containers")
    print("Computing a solution...\n")

    moves, finalGrid = aStar(grid, slotMatrix, containers, balanceFunc, craneStart=PARK_POS)
    if moves is None:
        print("No valid solution could be found.")
        logEvent("No valid balance solution could be found.")
        return None

    weightToContainer = {c['weight']: c for c in containers}
    
    numSteps = 0
    crane = PARK_POS
    tempGrid = [row[:] for row in grid]
    
    for src, dst in moves:
        if crane != src:
            numSteps += 1
        numSteps += 1
        if src != PARK_POS and 0 <= src[0] < ROWS and 0 <= src[1] < COLS:
            w = tempGrid[src[0]][src[1]]
            tempGrid[src[0]][src[1]] = "UNUSED"
            if dst != PARK_POS and 0 <= dst[0] < ROWS and 0 <= dst[1] < COLS:
                tempGrid[dst[0]][dst[1]] = w
        crane = dst
    
    if crane != PARK_POS:
        numSteps += 1
    
    print("Solution has been found, it will take")
    print(f"{numSteps} move{'s' if numSteps != 1 else ''}")

    totalTime = 0
    crane = PARK_POS
    tempGrid = [row[:] for row in grid]
    
    for src, dst in moves:
        if crane != src:
            d = manhattanDistance(crane, src)
            totalTime += d
        
        d = manhattanDistance(src, dst)
        totalTime += d
        
        if src != PARK_POS and 0 <= src[0] < ROWS and 0 <= src[1] < COLS:
            w = tempGrid[src[0]][src[1]]
            tempGrid[src[0]][src[1]] = "UNUSED"
            if dst != PARK_POS and 0 <= dst[0] < ROWS and 0 <= dst[1] < COLS:
                tempGrid[dst[0]][dst[1]] = w
        
        crane = dst
    
    if crane != PARK_POS:
        d = manhattanDistance(crane, PARK_POS)
        totalTime += d

    print(f"{totalTime} minutes (including movement from/to parked position)")
    logEvent(f"Balance solution found, it will require {numSteps} moves/{totalTime} minutes.")
    
    print("Hit ENTER when ready for first move:\n")
    input()

    step = 1
    crane = PARK_POS
    execGrid = [row[:] for row in grid]
    
    for src, dst in moves:
        # Case 1: Crane moves to source
        if crane != src:
            moveTime = manhattanDistance(crane, src)
            print(f"Step {step}: Move crane from {fmtCell(crane)} to {fmtCell(src)}, ({moveTime} minutes)")
            visMove(execGrid, cranePos=src)

            logEvent(f"Step {step}: Move crane from {fmtCell(crane)} to {fmtCell(src)}, ({moveTime} minutes)")

            input("Hit ENTER when done\n")
            step += 1
            crane = src

        # Case 2: Pick up and move container
        if src != PARK_POS and 0 <= src[0] < ROWS and 0 <= src[1] < COLS:
            cellValue = execGrid[src[0]][src[1]]
            containerInfo = weightToContainer.get(cellValue, None)
        else:
            containerInfo = None

        if containerInfo:
            moveTime = manhattanDistance(src, dst)
            print(f"Step {step}: Move '{containerInfo['description']}' from {fmtCell(src)} to {fmtCell(dst)}, ({moveTime} minutes)")

            visMove(execGrid, src=src, dst=dst, highlightMoving=True, highlightDestination=True)

            logEvent(f"Step {step}: Move '{containerInfo['description']}' from {fmtCell(src)} to {fmtCell(dst)}, ({moveTime} minutes)")

            if dst != PARK_POS and 0 <= dst[0] < ROWS and 0 <= dst[1] < COLS:
                execGrid[dst[0]][dst[1]] = cellValue
            if src != PARK_POS and 0 <= src[0] < ROWS and 0 <= src[1] < COLS:
                execGrid[src[0]][src[1]] = "UNUSED"
            containerInfo['pos'] = dst

            print("Press 'c' to add a comment, or just ENTER to continue: ", end='')
            userInput = input().strip().lower()
            if userInput == 'c':
                logUserComment()

            step += 1
            crane = dst

    # Case 3: Return crane to park
    if crane != PARK_POS:
        moveTime = manhattanDistance(crane, PARK_POS)
        print(f"Step {step}: Move crane from {fmtCell(crane)} to {fmtCell(PARK_POS)}, ({moveTime} minutes)")
        visMove(execGrid, cranePos=PARK_POS)

        logEvent(f"Step {step}: Move crane from {fmtCell(crane)} to {fmtCell(PARK_POS)}, ({moveTime} minutes)")

        input("Hit ENTER when done\n")
        step += 1

    return finalGrid

def fmtCell(rc):
    r, c = rc
    if r == PARK_POS[0] and c == PARK_POS[1]:
        return "park"
    return f"[{r+1:02d},{c+1:02d}]"


def main():
    logEvent("Program was started.")
    outName = None
    
    while True:
        print("-------------------------------------------------")
        filename = input("Enter a manifest: (or press ENTER to quit): ").strip()
        if filename == "":
            logEvent("Program was shut down.")
            if outName:
                saveLog(outName)
            else:
                saveLog("default")
            print("Goodbye.")
            break

        path = f"../P3_test_cases/{filename}"

        if not os.path.exists(path):
            print("File not found. Try again.")
            continue

        with open(path, "r") as f:
            lines = f.readlines()

        grid, slotExists, containers, contentsMap = parseManifest(lines)
        slotMatrix = buildSlotMatrix(slotExists)

        logEvent(f"Manifest {filename} is opened, there are {len(containers)} containers on the ship.")

        balanced, port, star = isShipBalanced(grid)
        
        vis(grid)
        
        if balanced:
            print("\nShip is already legally balanced.")
            logEvent("Ship is already balanced. No moves needed.")
            finalGrid = grid
        else:
            finalGrid = runInstructions(path, grid, slotMatrix, containers, isShipBalanced)
            if finalGrid is None:
                continue

        base = os.path.splitext(os.path.basename(path))[0]
        outName = base

        writeOutboundManifest(outName, lines, finalGrid, contentsMap, grid)

        print(f"\nI have written an updated manifest as {outName}OUTBOUND.txt")
        logEvent(f"Finished a Cycle. Manifest {outName}OUTBOUND.txt was written to the \n\tsolutions folder, and a reminder pop-up to the operator to send the file was displayed.")
        
        print("Don't forget to email it to the captain.")
        print("Hit ENTER when done.\n")
        input()


if __name__ == "__main__":
    main()