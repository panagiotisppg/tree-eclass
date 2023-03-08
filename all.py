from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def get_links(url:str, filter_words:list=[]):
     url = url.split()[0]
     # filter_words is used to ignore links that lead outside the subject's class
     filter_words += ['&sort', 'help.php?language=el&topic=documents', '#collapse0',
     'info/terms.php', 'info/privacy_policy.php', 'announcements/?course=',
     '/courses', 'modules/document/?course=', '&openDir=%', '/?course=', 'https://',
     'help.php?language=en&', 'topic=documents&subtopic', 'creativecommons.org/licenses']
     html_page = urlopen(Request(url))
     soup = BeautifulSoup(html_page, "lxml")
     all_links = [link.get('href') for link in soup.findAll('a')]

     files_tmp = []
     files = []
     directories = []
     directories_tmp = []
     directory_names = []

     for link in all_links:
          if all([x not in link for x in filter_words]):
               if 'http' not in link and link != '/':
                    link = 'https://eclass.aueb.gr'+link
                    if '&openDir=/ ' not in link+' ' and '&openDir= ' not in link+' ' and link != url:
                    # link is a file if it had . near the end else it's a directory
                         if '.' in link[-6:]:
                              files_tmp.append(link)
                         else:
                              directories_tmp.append(link)
                              
     file_names = [link.get('title') for link in soup.findAll('a') if link.get('title') != None]
     directory_names = [soup.find("a", href=dir_link.replace("https://eclass.aueb.gr", "")).text for dir_link in directories_tmp if soup.find("a", href=dir_link.replace("https://eclass.aueb.gr", "")) != None]

     for i in range(len(files_tmp)):
          files.append(f"{files_tmp[i]} {file_names[i]}")
     for i in range(len(directories_tmp)):
          directories.append(f"{directories_tmp[i]} {directory_names[i]}")
     return (files, directories)




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
        link = file.split()[0]
        name = ' '.join(file.split()[1:])
        print(f"{branch_prefix}{link} {name}")



import argparse

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