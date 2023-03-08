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
    files, directories = get_links(url)

    return [url, [gen_subtree(x) for x in directories], files]
tab_string = '      '

# WORKING WITH ONLY TAB SPACINGS
def print_tree(node, prefix='', is_last=True):
    # Print the prefix and node name
    print(f"{prefix}{tab_string if is_last else tab_string}{node[0]}")

    # Add the branch prefix
    branch_prefix = prefix + (tab_string if is_last else tab_string)

    # Print the directories
    for child in node[1]:
        print_tree(child, branch_prefix, child == node[1][-1])

    # Print the files
    for file in node[2]:
        print(f"{branch_prefix}{tab_string}{file}")


if __name__ == "__main__":
     print_tree(gen_subtree(url))