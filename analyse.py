from colorama import Back

def analyse(bit_str, hint:bool=False):
    if hint: print(f"***** {Back.GREEN} No. Leaf Nodes {Back.RESET} {Back.MAGENTA} Branch(0) / Leaf(1) {Back.RESET} {Back.RED} ASCII-EXTENDED Character {Back.RESET} {Back.BLUE} Encoded binary string {Back.RESET} *****\n")
    print(f"{Back.GREEN}{bit_str[:8]}{Back.RESET}", end="")
    cursor = 8
    found_leaves = 0
    while cursor < len(bit_str):
        print(f"{Back.MAGENTA}{bit_str[cursor]}{Back.RESET}", end="")
        if bit_str[cursor] == "0":
            cursor += 9
            found_leaves += 1
            print(f"{Back.RED}{bit_str[cursor-8:cursor]}{Back.RESET}", end="")            
            if found_leaves >= int(bit_str[:8], 2): break
        else:
            cursor += 1
    
    print(f"{Back.BLUE}{bit_str[cursor:]}{Back.RESET}")
            