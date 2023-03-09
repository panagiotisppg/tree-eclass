from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def get_links(url:str, filter_words:list=[]):
     working_url = url.split()[0]

     # filter_words is used to ignore links that lead outside the subject's class
     filter_words += ['&sort', 'help.php?language=el&topic=documents', '#collapse0',
     'info/terms.php', 'info/privacy_policy.php', 'announcements/?course=',
     '/courses', 'modules/document/?course=', '&openDir=%', '/?course=', 'https://',
     'help.php?language=en&', 'topic=documents&subtopic', 'creativecommons.org/licenses']
     html_page = urlopen(Request(working_url))
     soup = BeautifulSoup(html_page, "lxml")
     all_links = [link.get('href') for link in soup.findAll('a')]
     starting_title_name = soup.find("div", {"class": "panel-body"}).text.strip()
     starting_title_name = ''.join(starting_title_name.replace("\xa0", " ").strip().split("»")[-1:]).split("  ")[-1].strip()
     files_tmp, files, directories, directories_tmp, directory_names = [], [], [], [], []

     for link in all_links:
          if all([x not in link for x in filter_words]):
               if 'http' not in link and link != '/':
                    link = 'https://eclass.aueb.gr'+link
                    if '&openDir=/ ' not in link+' ' and '&openDir= ' not in link+' ' and link != working_url:
                    
                    # link is a file if it had . near the end else it's a directory
                         if '.' in link[-6:]:
                              files_tmp.append(link)
                         else:
                              directories_tmp.append(link)
                              
     file_names = [link.get('title') for link in soup.findAll('a') if link.get('title') != None]
     directory_names = [soup.find("a", href=dir_link.replace("https://eclass.aueb.gr", "")).text 
                         for dir_link in directories_tmp 
                         if soup.find("a", href=dir_link.replace("https://eclass.aueb.gr", "")) is not None]

     files = [f"{f} {starting_title_name}/{name} f" for f, name in zip(files_tmp, file_names)]
     directories = [f"{d} {name} d" for d, name in zip(directories_tmp, directory_names)]

     return (files, directories)