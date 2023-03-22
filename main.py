import argparse
import time
import requests
from bs4 import BeautifulSoup
from src.tree_utils import *
from src.downloading import *

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
        print('\n[\u001b[31m?\033[0m] KeyboardInterrupt. Aborting...\n', end = '\n\r')
        exit()