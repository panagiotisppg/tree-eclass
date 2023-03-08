from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

url = "https://eclass.aueb.gr/modules/document/?course=INF111"

# Get all sublinks from a given url where filter_words don't appear
def get_links(url:str, filter_words:list=[]):
    # filter_words is used to ignore links that lead outside the subject's class
    filter_words += ['&sort', 'help.php?language=el&topic=documents', '#collapse0',
                     'info/terms.php', 'info/privacy_policy.php', 'announcements/?course=',
                     '/courses', 'modules/document/?course=', '&openDir=%', '/?course=',
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

    return [url, [gen_subtree(x) for x in directories], files] # each object inside is a list of form [root, dirs, files]]

def print_tree(tree):
    parent, dir_children, file_children = tree
    print(parent, end='\f')
    print('\t', end='')
    for child in file_children:
        print(child, end='\f')
    for child in dir_children:
        print_tree(child)
    print('\b\b\b\b')



if __name__ == "__main__":
    # print(gen_subtree(url))

    example_output = ['https://eclass.aueb.gr/modules/document/?course=INF111', [['https://eclass.aueb.gr/modules/document/index.php?course=INF111&openDir=/633d42923lnj', [], ['https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/633d42923lnj/637bedc3rthH.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/633d42923lnj/633d4372ucxl.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/633d42923lnj/6357f5ccTTWb.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/633d42923lnj/63bc5adePYaL.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/633d42923lnj/63613f3c205f.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/633d42923lnj/638c574aPvq5.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/633d42923lnj/63974686vt4g.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/633d42923lnj/63a057adyqSI.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/633d42923lnj/63a057b7PBHd.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/633d42923lnj/63bd1a3dXIMY.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/633d42923lnj/637bedf5PHB3.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/633d42923lnj/63c559e0X4ed.rtf']], ['https://eclass.aueb.gr/modules/document/index.php?course=INF111&openDir=/616d557cShQK', [['https://eclass.aueb.gr/modules/document/index.php?course=INF111&openDir=/616d557cShQK/5faa6e5aTqdf', [['https://eclass.aueb.gr/modules/document/index.php?course=INF111&openDir=/616d557cShQK/5faa6e5aTqdf/5faa6f18uY2X', [], ['https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/616d557cShQK/5faa6e5aTqdf/5faa6f18uY2X/5faa762eOq6W.zip', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/616d557cShQK/5faa6e5aTqdf/5faa6f18uY2X/5faa7677f5zI.pdf']], ['https://eclass.aueb.gr/modules/document/index.php?course=INF111&openDir=/616d557cShQK/5faa6e5aTqdf/5fb4f97fxKVt', [], ['https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/616d557cShQK/5faa6e5aTqdf/5fb4f97fxKVt/5fb4f9c52BGr.zip', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/616d557cShQK/5faa6e5aTqdf/5fb4f97fxKVt/5fb4f9e8dVfe.pdf']]], ['https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/616d557cShQK/5faa6e5aTqdf/5faa6ecem90I.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/616d557cShQK/5faa6e5aTqdf/5fb4f7e8FPaE.pdf']], ['https://eclass.aueb.gr/modules/document/index.php?course=INF111&openDir=/616d557cShQK/6196459eN8In', [], ['https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/616d557cShQK/6196459eN8In/61964661VV4g.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/616d557cShQK/6196459eN8In/61964683Hz9I.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/616d557cShQK/6196459eN8In/619646e0HQfi.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/616d557cShQK/6196459eN8In/619b7c3da5L8.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/616d557cShQK/6196459eN8In/5fb8352an70B.zip']], ['https://eclass.aueb.gr/modules/document/index.php?course=INF111&openDir=/616d557cShQK/637cab560FpD', [], ['https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/616d557cShQK/637cab560FpD/637cac2a0MAu.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/616d557cShQK/637cab560FpD/637cabb4nPZG.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/616d557cShQK/637cab560FpD/637cb6ef1iig.zip']], ['https://eclass.aueb.gr/modules/document/index.php?course=INF111&openDir=/616d557cShQK/61a606af3pjk', [], ['https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/616d557cShQK/61a606af3pjk/637cb75aAhBI.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/616d557cShQK/61a606af3pjk/637cb791xv7S.zip']], ['https://eclass.aueb.gr/modules/document/index.php?course=INF111&openDir=/616d557cShQK/61b8840d9nW9', [], ['https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/616d557cShQK/61b8840d9nW9/61b885cfj0BY.csv', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/616d557cShQK/61b8840d9nW9/61b884648Oq2.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/616d557cShQK/61b8840d9nW9/61b88844fKOG.pdf']]], ['https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/616d557cShQK/6175a36bcW27.pdf']]], ['https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/63ff698a4mFk.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/63ea3ea2fU4i.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/633d43d0WwmP.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/63d905d09O6E.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/63d9059d6AZT.pdf', 'https://eclass.aueb.gr/modules/document/index.php?course=INF111&download=/63ff693bdFzt.pdf']]
    print_tree(example_output)