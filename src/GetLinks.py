from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

# get_links returns all the sublinks from a given url where all the filter_words don't appear
def get_links(url:str, filter_words:list=[]):
     # filter_words is used to ignore links that lead outside the subject's class
     filter_words += ['&sort', 'help.php?language=el&topic=documents', '#collapse0', 
                      'info/terms.php', 'info/privacy_policy.php', 'announcements/?course=', 
                      '/courses', 'modules/document/?course=', '&openDir=%', '/?course=',
                      'help.php?language=en&', 'topic=documents&subtopic', 'creativecommons.org/licenses']
     html_page = urlopen(Request(url))
     soup = BeautifulSoup(html_page, "lxml")
     all_links = [link.get('href') for link in soup.findAll('a')]
     out = []
     
     for link in all_links:
          if all([x not in link for x in filter_words]):
               if 'https://' not in link and link !=  '/':
                    link = 'https://eclass.aueb.gr'+link
                    if '&openDir=/ ' not in link+' ' and '&openDir= ' not in link+' ' and link != url:
                         # link is a file if it had . near the end  else it's a directory
                         if '.' in link[-6:]:
                              out.append(f"{link} f")
                         else:
                              out.append(f"{link} d")
     for el in out:
          file_or_directory = el.split()[1]
          if file_or_directory == 'f':
               out.append(out.pop(out.index(el)))
               break
     return out