import os
from readManifest import parseManifest
from manifest import writeOutboundManifest
from isBalanced import isShipBalanced
from AStar import aStar, buildSlotMatrix, manhattan_distance
from visualize import visualizeGrid as vis
from visualize import visMove
from logger import log_event, log_user_comment, save_log

ROWS = 8
COLS = 12
PARK_POS = (7, 0)  # Park at [08, 01] in display coordinates

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def run_instructions(path, grid, slotMatrix, containers, balanceFunc):
    print(f"\n{os.path.basename(path)} has {len(containers)} containers")
    print("Computing a solution...\n")

    moves, finalGrid = aStar(grid, slotMatrix, containers, balanceFunc, craneStart=PARK_POS)
    if moves is None:
        print("No valid solution could be found.")
        log_event("No valid balance solution could be found.")
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
            d = manhattan_distance(crane, src)
            total_time += d
        
        # Time to move container from source to destination
        d = manhattan_distance(src, dst)
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
        d = manhattan_distance(crane, PARK_POS)
        total_time += d

    print(f"{total_time} minutes (including movement from/to parked position)")
    log_event(f"Balance solution found, it will require {numSteps} moves/{total_time} minutes.")
    
    print("Hit ENTER when ready for first move:\n")
    input()

    # -------------------------
    # PRINT EXECUTION STEPS WITH FULL VISUALIZATION
    # -------------------------
    step = 1
    crane = PARK_POS
    execGrid = [row[:] for row in grid]  # Use ORIGINAL grid

    for src, dst in moves:
        # -------------------------
        # 1. Crane moves to source
        # -------------------------
        if crane != src:
            move_time = manhattan_distance(crane, src)
            print(f"{step}: Move crane from {fmt_cell(crane)} to {fmt_cell(src)} ({move_time} minutes)")
            visMove(execGrid, crane_pos=src)  # show crane moving, no container yet
            input("Hit ENTER when done\n")
            step += 1
            crane = src

        # -------------------------
        # 2. Pick up and move container
        # -------------------------
        if src != PARK_POS and 0 <= src[0] < ROWS and 0 <= src[1] < COLS:
            cell_value = execGrid[src[0]][src[1]]
            container_info = weight_to_container.get(cell_value, None)
        else:
            container_info = None

        if container_info:
            move_time = manhattan_distance(src, dst)
            print(f"{step}: Move '{container_info['description']}' from {fmt_cell(src)} to {fmt_cell(dst)} ({move_time} minutes)")

            # Show the move with highlighting:
            # - container being moved in green
            # - destination in red
            # - other containers in yellow
            # - unusable slots in black
            visMove(execGrid, src=src, dst=dst, highlight_moving=True, highlight_destination=True)

            log_event(f"{fmt_cell(src)} was moved to {fmt_cell(dst)}")

            # Update grid after move
            if dst != PARK_POS and 0 <= dst[0] < ROWS and 0 <= dst[1] < COLS:
                execGrid[dst[0]][dst[1]] = cell_value
            if src != PARK_POS and 0 <= src[0] < ROWS and 0 <= src[1] < COLS:
                execGrid[src[0]][src[1]] = "UNUSED"
            container_info['pos'] = dst

            # Offer option to add user comment
            print("Press 'c' to add a comment, or just ENTER to continue: ", end='')
            user_input = input().strip().lower()
            if user_input == 'c':
                log_user_comment()

            step += 1
            crane = dst

    # -------------------------
    # 3. Return crane to park
    # -------------------------
    if crane != PARK_POS:
        move_time = manhattan_distance(crane, PARK_POS)
        print(f"{step}: Move crane from {fmt_cell(crane)} to {fmt_cell(PARK_POS)} ({move_time} minutes)")
        visMove(execGrid, crane_pos=PARK_POS)  # visualize crane returning
        input("Hit ENTER when done\n")
        step += 1


    return finalGrid  # Return finalGrid for manifest writing

def fmt_cell(rc):
    r, c = rc
    # Check if this is the park position
    if r == PARK_POS[0] and c == PARK_POS[1]:
        return "park"
    return f"[{r+1:02d},{c+1:02d}]"


def main():
    log_event("Program was started.")
    
    while True:
        print("-------------------------------------------------")
        filename = input("Enter a manifest: (or press ENTER to quit): ").strip()
        if filename == "":
            log_event("Program was shut down.")
            save_log()
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

        log_event(f"Manifest {filename} is opened, there are {len(containers)} containers on the ship.")

        balanced, port, star = isShipBalanced(grid)
        
        vis(grid)
        
        if balanced:
            print("\nShip is already legally balanced.")
            log_event("Ship is already balanced. No moves needed.")
            finalGrid = grid
        else:
            finalGrid = run_instructions(path, grid, slotMatrix, containers, isShipBalanced)
            if finalGrid is None:
                continue

        # Clean output filename
        base = os.path.splitext(os.path.basename(path))[0]
        outName = base

        writeOutboundManifest(outName, lines, finalGrid, contents_map, grid)

        print(f"\nI have written an updated manifest as {outName}_OUTBOUND.txt")
        log_event(f"Finished a Cycle. Manifest {outName}_OUTBOUND.txt was written to desktop, and a reminder pop-up to operator to send file was displayed.")
        
        print("Don't forget to email it to the captain.")
        print("Hit ENTER when done.\n")
        input()


if __name__ == "__main__":
    main()