from src.GetLinks import get_links

i, loading_string, all_info = 1, "Generating tree structure ", []

# Generate directory tree for a given url
def gen_subtree(url):
    global i, loading_string
    files, directories = get_links(url)
    loading_string += '.'*i;     i+=1
    print(loading_string, end='\r')
    subtree = [url, [], files]
    for directory in directories:
        subtree[1].append(gen_subtree(directory))

    return subtree

# Print the directory tree
def print_tree(node, prefix='', is_last=True, tab_string='\t'):
    global all_info # all_info is going to be used for the local directory downloading...
    # Print the prefix and node name
    print(f"{prefix}{' '.join(node[0].split()[:-1])}"); all_info.append(f"{' '.join(node[0].split())}")

    # Add the branch prefix
    branch_prefix = prefix + (tab_string if is_last else tab_string)

    # Print the directories
    for child in node[1]:
        print_tree(child, branch_prefix, child == node[1][-1], tab_string)

    # Print the files
    for file in node[2]:
        link = file.split()[0]
        name = ' '.join(file.split()[1:-1])
        print(f"{branch_prefix}{link} {name}");    all_info.append(f"{link} {' '.join(file.split()[1:])}")