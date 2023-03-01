from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


def get_links(url):
     req = Request(url)
     html_page = urlopen(req)
     soup = BeautifulSoup(html_page, "lxml")
     start_links = []
     out = []
     for link in soup.findAll('a'):
          start_links.append(link.get('href'))

     for link in start_links:
          
          if '&sort' not in link and 'help.php?language=el&topic=documents' not in link and '#collapse0' not in link and 'info/terms.php' not in link and 'info/privacy_policy.php' not in link and 'announcements/?course=' not in link and '/courses' not in link and 'modules/document/?course=' not in link and '&openDir=%' not in link and '/?course=' not in link:
               
               if 'https://' not in link and link !=  '/':
                    
                    link = 'https://eclass.aueb.gr'+link
                    
                    if '&openDir=/ ' not in link+' ' and '&openDir= ' not in link+' ' and link != url:
                         if '.' in link[-5:]:
                              out.append(f"{link} f")
                         else:
                              out.append(f"{link} d")
     return out



print('\n'+url)
# SAVE
out = []
next_links0 = get_links(url)
print(f"\t│")
for link1 in next_links0:
     if link1 == next_links0[-1]:
          print("\t└-> "+link1+'\n')
     else:
          print('\t├-> '+link1)

     if link1.split()[1] == 'd':
          print(f"\t│\t│")
          next_links1 = get_links(link1.split()[0])
          for link2 in next_links1:
               if link2 == next_links1[-1]:
                    print("\t│\t└-> "+link2+'\n\t│')
               else:
                    print('\t│\t├-> '+link2)

               if link2.split()[1] == 'd':
                    print(f"\t│\t│\t│")
                    next_links2 = get_links(link2.split()[0])
                    for link3 in next_links2:
                         if link3 == next_links2[-1]:
                              print("\t│\t│\t└-> "+link3+'\n\t│\t│')
                         else:
                              print('\t│\t│\t├-> '+link3)

                         if link3.split()[1] == 'd':
                              print(f"\t│\t│\t│\t│")
                              next_links3 = get_links(link3.split()[0])
                              for link4 in next_links3:
                                   if link4 == next_links3[-1]:
                                        print("\t│\t│\t│\t└-> "+link4+'\n\t│\t│\t│')
                                   else:
                                        print('\t│\t│\t│\t├-> '+link4)

                                   if link4.split()[1] == 'd':
                                        print(f"\t│\t│\t│\t│\t│")
                                        next_links4 = get_links(link4.split()[0])
                                        for link5 in next_links4:
                                             if link5 == next_links4[-1]:
                                                  print("\t│\t│\t│\t│\t└-> "+link5+'\n\t│\t│\t│\t│')
                                             else:
                                                  print('\t│\t│\t│\t│\t├-> '+link5)    
                                                     
                                             if link5.split()[1] == 'd':
                                                  print(f"\t│\t│\t│\t│\t│\t│")
                                                  next_links5 = get_links(link5.split()[0])
                                                  for link6 in next_links5:
                                                       if link6 == next_links5[-1]:
                                                            print("\t│\t│\t│\t│\t│\t└-> "+link6+'\n\t│\t│\t│\t│\t│')
                                                       else:
                                                            print('\t│\t│\t│\t│\t│\t├-> '+link6)
