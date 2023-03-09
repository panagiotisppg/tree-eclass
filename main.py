import argparse
import time
from src.tree_utils import *

if __name__ == "__main__":
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Generate a eclass.aueb directory tree for a given the INF number')
    parser.add_argument('-t', '--tab-string', type=str, default='\t', help='The string used for indentation (default: \\t)')
    parser.add_argument('-I', '--INF', type=str, required=True, help='The eclass INF number to generate the directory tree from')
    args = parser.parse_args()
    url = f"https://eclass.aueb.gr/modules/document/?course=INF{args.INF} Starting Link"
    # Generate the directory tree
    print('Generating tree structure ', end='\r');    start_time = time.time()
    tree = gen_subtree(url)
    delta_time = time.time() - start_time;
    print(f"\nDone! Took a total of {delta_time:.2f} seconds to get the info.\n")
    # Print the directory tree
    print_tree(tree, tab_string=args.tab_string)
    print('\n'.join(all_info))