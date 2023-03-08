from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

url = "https://eclass.aueb.gr/modules/document/?course=INF111"

# Get all sublinks from a given url where filter_words don't appear
def get_links(url:str, filter_words:list=[]):
     # filter_words is used to ignore links that lead outside the subject's class
     filter_words += ['&sort', 'help.php?language=el&topic=documents', '#collapse0',
     'info/terms.php', 'info/privacy_policy.php', 'announcements/?course=',
     '/courses', 'modules/document/?course=', '&openDir=%', '/?course=', 'https://',
     'help.php?language=en&', 'topic=documents&subtopic', 'creativecommons.org/licenses']
     html_page = urlopen(Request(url))
     soup = BeautifulSoup(html_page, "lxml")
     all_links = [link.get('href') for link in soup.findAll('a')]
     files = []
     directories = []

     for link in all_links:
          if all([x not in link for x in filter_words]):
               if 'http' not in link and link != '/':
                    link = 'https://eclass.aueb.gr'+link
                    if '&openDir=/ ' not in link+' ' and '&openDir= ' not in link+' ' and link != url:
                    # link is a file if it had . near the end else it's a directory
                         if '.' in link[-6:]:
                              files.append(link)
                         else:
                              directories.append(link)

     return (files, directories)

# Generate directory tree for a given url

def gen_subtree(url):
    subtree = [url, [], []] # each object inside is a list of form [root, dirs, files]]

    files, directories = get_links(url)

    return [url, [gen_subtree(x) for x in directories], files]

def print_tree(node, prefix='', is_last=True):
    # Recursively print the node and its children like the structure of the UNIX command tree.
    
    # Print the prefix and node name
    print(prefix + ('\t' if is_last else '\t') + node[0])

    # Add the branch prefix. Depending on whether the node is the last of the directory or not
    branch_prefix = prefix + ('\t' if is_last else '\t')

    # Print the directories
    for i, child in enumerate(node[1]):
        # Check if is_last
        is_last_child = i == len(node[1]) - 1
        print_tree(child, branch_prefix, is_last_child)

    # Print the files
    for file in node[2]:
        print(branch_prefix + '\t' + file)


'''
def print_tree(node, prefix='', is_last=True, depth=0):
    # Print the prefix and node name
    print(prefix + ('└── ' if is_last else '├── ') + node[0])

    # Add the branch prefix
    branch_prefix = prefix + ('    ' if is_last else '│   ')

    # Print the directories
    for i, child in enumerate(node[1]):
        is_last_child = i == len(node[1]) - 1
        print_tree(child, branch_prefix + ('│   ' if is_last else '    '), is_last_child, depth + 1)

	# Print the files
    for file in node[2]:
        print(branch_prefix + ('│   ' if not is_last else '    ') + '├── ' + file)
'''

if __name__ == "__main__":
     print_tree(gen_subtree(url))
