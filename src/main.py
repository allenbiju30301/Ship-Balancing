import re
from visualize import visualize_grid as vis
from readManifest import parse_manifest as read
from isBalanced import is_ship_balanced as balance

ROWS = 8
COLS = 12

def main():
    filename = input("Enter a manifest: ").strip()
    filepath = f"../P3_test_cases/{filename}"
    filename = filename.split('.txt')[0]
    
    with open(filepath, "r") as f:
        lines = f.readlines()

    grid, slot_exists, containers = read(lines)

    print(f"{(filename)} has {len(containers)} containers.")

    vis(grid)
    
    balanced, port_weight, starboard_weight = balance(grid)
    
    print("\nBalance Check:")
    if balanced:
        print("The ship is legally balanced!")
        #IMMEDIATELY WRITE TO THE MANIFEST AND RETURN 0
    else:
        print("The ship is NOT legally balanced.\n")
        # start balancing!!!!
        
        
    
    
    
    # for now we will output a new file, but 
    # before we submit make sure we adjust the input file!

if __name__ == "__main__":
    main()
