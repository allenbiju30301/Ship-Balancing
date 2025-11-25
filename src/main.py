import os
from readManifest import parseManifest
from manifest import writeOutboundManifest
from isBalanced import isShipBalanced
from AStar import aStar, buildSlotMatrix

# Crane is parked ABOVE row 1, column 8 → treat row = -1
PARK_POS = (-1, 7)


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def fmt_cell(rc):
    """Convert 0-indexed grid coords to manifest coords."""
    r, c = rc
    return f"[{r+1:02d},{c+1:02d}]"


def run_instructions(path, grid, slotMatrix, containers, balanceFunc):

    print(f"\n{os.path.basename(path)} has {len(containers)} containers")
    print("Computing a solution...\n")

    moves, finalGrid = aStar(grid, slotMatrix, containers, balanceFunc, craneStart=PARK_POS)

    if moves is None:
        print("No valid solution could be found.")
        return None

    numMoves = len(moves)

    print("Solution has been found, it will take")
    print(f"{numMoves} move{'s' if numMoves != 1 else ''}")

    # -------------------------
    # TIME CALCULATION
    # -------------------------
    total_time = 0
    crane = PARK_POS

    if numMoves > 0:

        # Park → first source
        first_src = moves[0][0]
        total_time += manhattan(crane, first_src)
        crane = first_src

        # Each container move
        for (src, dst) in moves:
            total_time += manhattan(src, dst)
            crane = dst

        # Return to park
        total_time += manhattan(crane, PARK_POS)

    print(f"{total_time} minutes (including movement from/to parked position)")
    print("Hit ENTER when ready for first move\n")
    input()

    # --------------------------------
    # PRINT EXECUTION STEPS
    # --------------------------------

    if numMoves == 0:
        print("1 of 1: Crane is already parked and no moves are needed.\n")
        return finalGrid

    total_steps = numMoves + 2
    step = 1

    # Step 1: park → first source
    first_src = moves[0][0]
    print(f"{step} of {total_steps}: Move crane from park to {fmt_cell(first_src)}")
    print("Hit ENTER when done\n")
    input()
    step += 1

    # Middle steps: actual container moves
    for (src, dst) in moves:
        print(f"{step} of {total_steps}: Move from {fmt_cell(src)} to {fmt_cell(dst)}")
        print("Hit ENTER when done\n")
        input()
        step += 1

    # Final step: return to park
    last_dst = moves[-1][1]
    print(f"{step} of {total_steps}: Move from {fmt_cell(last_dst)} to park")
    print("Hit ENTER when done\n")
    input()

    return finalGrid


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

        if balanced:
            print("\nShip is already legally balanced.")
            finalGrid = grid
        else:
            finalGrid = run_instructions(path, grid, slotMatrix, containers, isShipBalanced)
            if finalGrid is None:
                continue

        # Clean output filename — NO double _OUTBOUND
        base = os.path.splitext(os.path.basename(path))[0]
        outName = base

        writeOutboundManifest(outName, lines, finalGrid, contents_map)

        print(f"\nI have written an updated manifest as {outName}_OUTBOUND.txt")
        print("Don't forget to email it to the captain.")
        print("Hit ENTER when done.\n")
        input()


if __name__ == "__main__":
    main()






















# import re
# from visualize import visualizeGrid as vis
# from manifest import parseManifest as read
# from manifest import writeOutboundManifest as write
# from isBalanced import isShipBalanced as balance
# from AStar import aStar
# from AStar import buildSlotMatrix

# ROWS = 8
# COLS = 12

# def main():
#     filename = input("Enter a manifest: ").strip()
#     filepath = f"../P3_test_cases/{filename}"
#     shortname = filename.split('.txt')[0]

#     with open(filepath, "r") as f:
#         lines = f.readlines()

#     grid, slotExistsDict, containers, contentsMap = read(lines)
#     slotMatrix = buildSlotMatrix(slotExistsDict)

#     print(f"{shortname} has {len(containers)} containers.\n")

#     vis(grid)

#     balanced, portWeight, starboardWeight = balance(grid)

#     print("\nBalance Check:")
#     if balanced:
#         print("Ship is already legally balanced. Writing outbound manifest...")
#         write(shortname, lines, grid, contentsMap)
#         return
#     else:
#         print("Ship is NOT legally balanced.\nStarting A* search...\n")

#     # A* search
#     path, finalGrid = aStar(grid, slotMatrix, containers, balance, craneStart=(1,9)) # just above (1, 8)

#     if path is None:
#         print("No balancing solution found.")
#         return

#     print(f"Found solution in {len(path)} moves:")
#     for i, (src, dst) in enumerate(path, 1):
#         print(f"{i}. Move {src} -> {dst}")

#     vis(finalGrid)

#     write(shortname, lines, finalGrid, contentsMap)

# if __name__ == "__main__":
#     main()