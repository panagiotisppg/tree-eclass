from src.GetLinks import get_links

def gen_tree(url):
     print('\n'+url)

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
