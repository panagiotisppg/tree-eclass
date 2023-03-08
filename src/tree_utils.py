from src.GetLinks import get_links

# Generate directory tree for a given url
def gen_subtree(url):
    files, directories = get_links(url)

    subtree = [url, [], files]
    for directory in directories:
        subtree[1].append(gen_subtree(directory))

    return subtree

# Print the directory tree
def print_tree(node, prefix='', is_last=True, tab_string='\t'):
    # Print the prefix and node name
    print(f"{prefix}{node[0]}")

    # Add the branch prefix
    branch_prefix = prefix + (tab_string if is_last else tab_string)

    # Print the directories
    for child in node[1]:
        print_tree(child, branch_prefix, child == node[1][-1], tab_string)

    # Print the files
    for file in node[2]:
        print(f"{branch_prefix}{file}")