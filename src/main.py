import re
from visualize import visualizeGrid as vis
from manifest import parseManifest as read
from manifest import writeOutboundManifest as write
from isBalanced import isShipBalanced as balance
from AStar import aStar
from AStar import buildSlotMatrix

ROWS = 8
COLS = 12

def main():
    filename = input("Enter a manifest: ").strip()
    filepath = f"../P3_test_cases/{filename}"
    shortname = filename.split('.txt')[0]

    with open(filepath, "r") as f:
        lines = f.readlines()

    grid, slotExistsDict, containers, contentsMap = read(lines)
    slotMatrix = buildSlotMatrix(slotExistsDict)

    print(f"{shortname} has {len(containers)} containers.\n")

    vis(grid)

    balanced, portWeight, starboardWeight = balance(grid)

    print("\nBalance Check:")
    if balanced:
        print("Ship is already legally balanced. Writing outbound manifest...")
        write(shortname, lines, grid, contentsMap)
        return
    else:
        print("Ship is NOT legally balanced.\nStarting A* search...\n")

    # A* search
    path, finalGrid = aStar(grid, slotMatrix, containers, balance, craneStart=(1,9)) # just above (1, 8)

    if path is None:
        print("No balancing solution found.")
        return

    print(f"Found solution in {len(path)} moves:")
    for i, (src, dst) in enumerate(path, 1):
        print(f"{i}. Move {src} -> {dst}")

    vis(finalGrid)

    write(shortname, lines, finalGrid, contentsMap)

if __name__ == "__main__":
    main()
