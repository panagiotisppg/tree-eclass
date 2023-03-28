from src.GetLinks import get_links, custom_print

i, loading_string, all_info = 1, "[\u001b[32m+\033[0m] Gathering eclass course info ", []

# Generate directory tree for a given url
def gen_subtree(url, print_enabled=True):
    global i, loading_string
    files, directories = get_links(url)

    loading_string += '.'*i;     i+=1
    custom_print(print_enabled, loading_string, end='\r')

    subtree = [url, [], files]
    for directory in directories:
        subtree[1].append(gen_subtree(directory, print_enabled))

    return subtree

# Print the directory tree
def print_tree(node, prefix='', is_last=True, tab_string='\t', print_enabled=True):
    # global all_info # all_info is going to be used for the local directory downloading...
    # Print the prefix and node name
    custom_print(print_enabled, f"{prefix}{' '.join(node[0].split()[:-1])}"); all_info.append(f"{' '.join(node[0].split())}")

    # Add the branch prefix
    branch_prefix = prefix + (tab_string if is_last else tab_string)

    # Print the directories
    for child in node[1]:
        print_tree(child, branch_prefix, child == node[1][-1], tab_string, print_enabled)

    # Print the files
    for file in node[2]:
        link = file.split()[0]
        name = ' '.join(file.split()[1:-1])
        file_extension = '.'+''.join(link.split('/')[-1].split('.')[1:])
        if file_extension in name:    file_extension = ''
        custom_print(print_enabled, f"{branch_prefix}{link} {name}{file_extension}", print_enabled);    all_info.append(f"{link} {' '.join(file.split()[1:-1])}{file_extension} {' '.join(file.split()[-1])}")