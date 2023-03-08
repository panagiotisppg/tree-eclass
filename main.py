import argparse
from src.tree_utils import *

if __name__ == "__main__":
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Generate a eclass.aueb directory tree for a given the INF number')
    parser.add_argument('-t', '--tab-string', type=str, default='\t', help='The string used for indentation (default: \\t)')
    parser.add_argument('-I', '--INF', type=str, required=True, help='The eclass INF number to generate the directory tree from')
    args = parser.parse_args()
    url = f"https://eclass.aueb.gr/modules/document/?course=INF{args.INF} Starting Link"
    # Generate the directory tree
    tree = gen_subtree(url)
    print('Generating tree structure')
    # Print the directory tree
    print_tree(tree, tab_string=args.tab_string)