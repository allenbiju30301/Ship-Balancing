import os
from readManifest import parseManifest
from manifest import writeOutboundManifest
from isBalanced import isShipBalanced
from AStar import aStar, buildSlotMatrix, bfs_distance
from visualize import visualizeGrid as vis

ROWS = 8
COLS = 12
PARK_POS = (ROWS, 0)

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def run_instructions(path, grid, slotMatrix, containers, balanceFunc):
    print(f"\n{os.path.basename(path)} has {len(containers)} containers")
    print("Computing a solution...\n")

    moves, finalGrid = aStar(grid, slotMatrix, containers, balanceFunc, craneStart=PARK_POS)
    if moves is None:
        print("No valid solution could be found.")
        return None

    weight_to_container = {c['weight']: c for c in containers}
    
    # Count total number of steps (crane movements + container movements + return to park)
    numSteps = 0
    crane = PARK_POS
    tempGrid = [row[:] for row in grid]
    
    for src, dst in moves:
        # Count crane movement to source (if needed)
        if crane != src:
            numSteps += 1
        # Count container move
        numSteps += 1
        # Update position for next iteration
        if src != PARK_POS and 0 <= src[0] < ROWS and 0 <= src[1] < COLS:
            w = tempGrid[src[0]][src[1]]
            tempGrid[src[0]][src[1]] = "UNUSED"
            if dst != PARK_POS and 0 <= dst[0] < ROWS and 0 <= dst[1] < COLS:
                tempGrid[dst[0]][dst[1]] = w
        crane = dst
    
    # Count return to park
    if crane != PARK_POS:
        numSteps += 1
    
    print("Solution has been found, it will take")
    print(f"{numSteps} move{'s' if numSteps != 1 else ''}")

    # Compute total time by simulating the execution with the original grid
    total_time = 0
    crane = PARK_POS
    tempGrid = [row[:] for row in grid]  # Start with original grid state
    
    for src, dst in moves:
        # Time to move crane to source
        if crane != src:
            d = bfs_distance(tempGrid, crane, src, ignoreContainers=True)
            if d is not None:
                total_time += d
        
        # Time to move container from source to destination
        d = bfs_distance(tempGrid, src, dst, ignoreContainers=False)
        if d is not None:
            total_time += d
        
        # Update temp grid to reflect the move
        if src != PARK_POS and 0 <= src[0] < ROWS and 0 <= src[1] < COLS:
            w = tempGrid[src[0]][src[1]]
            tempGrid[src[0]][src[1]] = "UNUSED"
            if dst != PARK_POS and 0 <= dst[0] < ROWS and 0 <= dst[1] < COLS:
                tempGrid[dst[0]][dst[1]] = w
        
        crane = dst
    
    # Time to return crane to park
    if crane != PARK_POS:
        d = bfs_distance(tempGrid, crane, PARK_POS, ignoreContainers=True)
        if d is not None:
            total_time += d

    print(f"{total_time} minutes (including movement from/to parked position)")
    print("Hit ENTER when ready for first move\n")
    input()

    # -------------------------
    # PRINT EXECUTION STEPS
    # -------------------------
    step = 1
    crane = PARK_POS
    execGrid = [row[:] for row in grid]  # Use ORIGINAL grid, not finalGrid
    
    for src, dst in moves:
        # Move crane from park/current position to source
        if crane != src:
            move_time = bfs_distance(execGrid, crane, src, ignoreContainers=True)
            if move_time:
                print(f"{step}: Move crane from {fmt_cell(crane)} to {fmt_cell(src)} ({move_time} minutes)")
                input("Hit ENTER when done\n")
                step += 1
            crane = src

        # Pick up and move container
        if src != PARK_POS and 0 <= src[0] < ROWS and 0 <= src[1] < COLS:
            cell_value = execGrid[src[0]][src[1]]
            container_info = weight_to_container.get(cell_value, None)
        else:
            container_info = None

        if container_info:
            move_time = bfs_distance(execGrid, src, dst, ignoreContainers=False)
            if move_time:
                print(f"{step}: Move '{container_info['description']}' from {fmt_cell(src)} to {fmt_cell(dst)} ({move_time} minutes)")
                # Update execGrid to reflect the move
                if dst != PARK_POS and 0 <= dst[0] < ROWS and 0 <= dst[1] < COLS:
                    execGrid[dst[0]][dst[1]] = cell_value
                if src != PARK_POS and 0 <= src[0] < ROWS and 0 <= src[1] < COLS:
                    execGrid[src[0]][src[1]] = "UNUSED"
                container_info['pos'] = dst
                input("Hit ENTER when done\n")
                step += 1
                crane = dst

    # Return crane to park
    if crane != PARK_POS:
        move_time = bfs_distance(execGrid, crane, PARK_POS, ignoreContainers=True)
        if move_time:
            print(f"{step}: Move crane from {fmt_cell(crane)} to {fmt_cell(PARK_POS)} ({move_time} minutes)")
            input("Hit ENTER when done\n")
            step += 1

    return finalGrid  # Return finalGrid for manifest writing

def fmt_cell(rc):
    r, c = rc
    if r == ROWS:
        return "park"
    return f"[{r+1:02d},{c+1:02d}]"


def main():
    while True:
        print("-------------------------------------------------")
        filename = input("Enter a manifest: (or press ENTER to quit): ").strip()
        if filename == "":
            print("Goodbye.")
            break

        path = f"../P3_test_cases/{filename}"

        if not os.path.exists(path):
            print("File not found. Try again.")
            continue

        with open(path, "r") as f:
            lines = f.readlines()

        grid, slotExists, containers, contents_map = parseManifest(lines)
        slotMatrix = buildSlotMatrix(slotExists)

        balanced, port, star = isShipBalanced(grid)
        
        vis(grid)
        
        if balanced:
            print("\nShip is already legally balanced.")
            finalGrid = grid
        else:
            finalGrid = run_instructions(path, grid, slotMatrix, containers, isShipBalanced)
            if finalGrid is None:
                continue

        # Clean output filename
        base = os.path.splitext(os.path.basename(path))[0]
        outName = base

        writeOutboundManifest(outName, lines, finalGrid, contents_map)

        print(f"\nI have written an updated manifest as {outName}_OUTBOUND.txt")
        print("Don't forget to email it to the captain.")
        print("Hit ENTER when done.\n")
        input()


if __name__ == "__main__":
    main()