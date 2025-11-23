import re
from visualize import visualize_grid as vis
from readManifest import parse_manifest as read
from isBalanced import is_ship_balanced as balance
from AStar import AStar

ROWS = 8
COLS = 12

def write_outbound_manifest(filename, lines, final_grid, contents_map):
    outname = filename + "OUTBOUND.txt"
    output = []

    index = 0
    for line in lines:
        # Match coordinate lines
        if re.match(r"\[\d{2},\d{2}\]", line):

            r = index // COLS + 1
            c = index % COLS + 1

            val = final_grid[r-1][c-1]

            # Weight formatting
            if val == "NAN":
                weight_str = "00000"
            elif val == "UNUSED":
                weight_str = "00000"
            else:
                weight_str = f"{val:05d}"

            english = contents_map[(r, c)]

            new_line = f"[{r:02d},{c:02d}], {{{weight_str}}}, {english}\n"
            output.append(new_line)

            index += 1

        else:
            # Copy comment/header lines untouched
            output.append(line)

    with open(outname, "w") as f:
        f.writelines(output)

    print(f"\nWrote outbound manifest: {outname}")


def build_slot_matrix(slot_exists_dict):
    matrix = [[False for _ in range(COLS)] for _ in range(ROWS)]
    for r in range(ROWS):
        for c in range(COLS):
            key = (r+1, c+1)
            matrix[r][c] = slot_exists_dict.get(key, False)
    return matrix


def main():
    filename = input("Enter a manifest: ").strip()
    filepath = f"../P3_test_cases/{filename}"
    shortname = filename.split('.txt')[0]

    with open(filepath, "r") as f:
        lines = f.readlines()

    # NEW: contents_map
    grid, slot_exists_dict, containers, contents_map = read(lines)
    slot_matrix = build_slot_matrix(slot_exists_dict)

    print(f"{shortname} has {len(containers)} containers.\n")

    vis(grid)

    balanced, port_weight, starboard_weight = balance(grid)

    print("\nBalance Check:")
    if balanced:
        print("Ship is already legally balanced. Writing outbound manifest...")
        write_outbound_manifest(shortname, lines, grid, contents_map)
        return
    else:
        print("Ship is NOT legally balanced.\nStarting A* search...\n")

    # A* search
    path, final_grid = AStar(grid, slot_matrix, containers, balance)

    if path is None:
        print("No balancing solution found.")
        return

    print(f"Found solution in {len(path)} moves:")
    for i, (src, dst) in enumerate(path, 1):
        print(f"{i}. Move {src} -> {dst}")

    vis(final_grid)

    write_outbound_manifest(shortname, lines, final_grid, contents_map)


if __name__ == "__main__":
    main()













# import re
# from visualize import visualize_grid as vis
# from readManifest import parse_manifest as read
# from isBalanced import is_ship_balanced as balance

# ROWS = 8
# COLS = 12

# def main():
#     filename = input("Enter a manifest: ").strip()
#     filepath = f"../P3_test_cases/{filename}"
#     filename = filename.split('.txt')[0]
    
#     with open(filepath, "r") as f:
#         lines = f.readlines()

#     grid, slot_exists, containers = read(lines)

#     print(f"{(filename)} has {len(containers)} containers.")

#     vis(grid)
    
#     balanced, port_weight, starboard_weight = balance(grid)
    
#     print("\nBalance Check:")
#     if balanced:
#         print("The ship is legally balanced!")
#         #IMMEDIATELY WRITE TO THE MANIFEST AND RETURN 0
#     else:
#         print("The ship is NOT legally balanced.\n")
#         # start balancing!!!!
        
        
    
    
    
#     # for now we will output a new file, but 
#     # before we submit make sure we adjust the input file!

# if __name__ == "__main__":
#     main()
