import argparse
import os
import time
import requests
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

i, loading_string, all_info = 1, "[\u001b[32m+\033[0m] Gathering eclass course info ", []

# Generate directory tree for a given url
def gen_subtree(url):
    global i, loading_string
    files, directories = get_links(url)

    loading_string += '.'*i;     i+=1
    print(loading_string, end='\r')
    
    subtree = [url, [], files]
    for directory in directories:
        subtree[1].append(gen_subtree(directory))

    return subtree

# Print the directory tree
def print_tree(node, prefix='', is_last=True, tab_string='\t'):
    global all_info # all_info is going to be used for the local directory downloading...
    # Print the prefix and node name
    print(f"{prefix}{' '.join(node[0].split()[:-1])}"); all_info.append(f"{' '.join(node[0].split())}")

    # Add the branch prefix
    branch_prefix = prefix + (tab_string if is_last else tab_string)

    # Print the directories
    for child in node[1]:
        print_tree(child, branch_prefix, child == node[1][-1], tab_string)

    # Print the files
    for file in node[2]:
        link = file.split()[0]
        name = ' '.join(file.split()[1:-1])
        file_extension = '.'+''.join(link.split('/')[-1].split('.')[1:])
        if file_extension in name:    file_extension = ''
        print(f"{branch_prefix}{link} {name}{file_extension}");    all_info.append(f"{link} {' '.join(file.split()[1:-1])}{file_extension} {' '.join(file.split()[-1])}")

def download_files(to_download, download_dir="."):
    dir_translation = {}
    try:
        if '~/Desktop/' in download_dir and download_dir.count('/') == 2:
            os.chdir(os.path.join(os.path.expanduser("~"), "Desktop"))
            download_dir = '/'.join(download_dir.split('/')[-1:])
        else:
            os.mkdir(download_dir.split('/')[-1])
            os.chdir(download_dir.split('/')[-1])
    except FileNotFoundError:
        print('[\u001b[31m?\033[0m] Failed to locate directory. Aborting...')
        exit()
    for element in to_download:
        if element[-1] == 'd':
            dir_translation[''.join(element.split()[0].split('&openDir=')[1:]).split('/')[-1]] = ' '.join(element.split()[1:-1])
    for element in to_download:
        if element[-1] == 'd':
            link_of_dir = element.split()[0]
            name_of_dir = ' '.join(element.split()[1:-1])
            path = ''.join(link_of_dir.split('&openDir=')[1:]).split('/')[1:]
            translated_path = [dir_translation[path_element] for path_element in path]
            if not os.path.isdir(f"{download_dir}/{'/'.join(translated_path)}"):
                os.mkdir(f"{download_dir}/{'/'.join(translated_path)}")
    
    for element in to_download:
        if element[-1] == 'f':
            link_of_file = element.split()[0]
            name_of_file = ''.join(' '.join(element.split()[1:-1]).split('/')[1:]).replace('..', '.')
            path = ''.join(link_of_file.split('&download=')[1:]).split('/')[1:-1]
            translated_path = [dir_translation[path_element] for path_element in path]
            response = requests.get(link_of_file)
            open(f"{download_dir}/{'/'.join(translated_path)}/{name_of_file}".replace('//', '/'), "wb").write(response.content)
            print(f"[\u001b[32m+\033[0m] Downloaded {download_dir}/{'/'.join(translated_path)}/{name_of_file}".replace('//', '/'))

if __name__ == "__main__":
    try:
        # Parse the command line arguments
        parser = argparse.ArgumentParser(description='Generate a eclass.aueb directory tree for a given the INF number')
        parser.add_argument('-T', '--tab-string', type=str, default='\t', help='The string used for indentation (default: \\t)')
        parser.add_argument('-C', '--course', type=str, required=True, help='The eclass id number (ex. INF111) to generate the directory tree from')
        args = parser.parse_args()
        
        # Start generating the directory tree
        print(f'[\u001b[32m+\033[0m] Gathering eclass course info ', end='\r');    start_time = time.time()

        # Get starting page title
        try:
            response = requests.get(f"https://eclass.aueb.gr/courses/{args.course}/");    soup = BeautifulSoup(response.content, 'html.parser');    h1_tag = soup.find('h1', class_='page-title');    course_title = h1_tag.text.strip()
        except AttributeError:
            print(f"[\u001b[31m?\033[0m] Failed to get class name, initializing value with: {args.course}.\n")
            course_title = args.course
        url = f"https://eclass.aueb.gr/modules/document/?course={args.course} {course_title} d"

        tree = gen_subtree(url)
        delta_time = time.time() - start_time;
        print(f"\n[\u001b[32m+\033[0m] Done! Took a total of {delta_time:.2f} seconds to get the info.\n")
        
        # Print the directory tree
        print_tree(tree, tab_string=args.tab_string)
        # print('\n'.join(all_info))
        download_eclass = str(input("\n\n[\u001b[33m?\033[0m] Do you want to download the files of the subject to your local machine? [Y/n] "))
        if 'Y' in download_eclass.upper():
            download_location = str(input(f"[\u001b[33m/\033[0m] Where should the files get downloaded? (All files, folders and subfolders are going to be downloaded to a created folder)\n[\u001b[33m?\033[0m] (Default: ~/Desktop/{course_title}): "))
            print()
            if download_location == '': 
                download_files(all_info, f"~/Desktop/{course_title}")
            else:
                download_files(all_info, download_location)
    except KeyboardInterrupt:
        print('[\u001b[31m?\033[0m] KeyboardInterrupt. Aborting...', end = '\n\r')
        exit()