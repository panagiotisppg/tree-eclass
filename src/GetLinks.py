from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

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