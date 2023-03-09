import argparse
import time
import requests
from bs4 import BeautifulSoup
from src.tree_utils import *
from src.downloading import *

if __name__ == "__main__":
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Generate a eclass.aueb directory tree for a given the INF number')
    parser.add_argument('-t', '--tab-string', type=str, default='\t', help='The string used for indentation (default: \\t)')
    parser.add_argument('-I', '--INF', type=str, required=True, help='The eclass INF number to generate the directory tree from')
    args = parser.parse_args()
    
    # Start generating the directory tree
    print(f'Gathering eclass course info ', end='\r');    start_time = time.time()

    # Get starting page title
    response = requests.get(f"https://eclass.aueb.gr/courses/INF{args.INF}/");    soup = BeautifulSoup(response.content, 'html.parser');    h1_tag = soup.find('h1', class_='page-title');    course_title = h1_tag.text.strip()
    url = f"https://eclass.aueb.gr/modules/document/?course=INF{args.INF} {course_title} d"

    tree = gen_subtree(url)
    delta_time = time.time() - start_time;
    print(f"\n[+] Done! Took a total of {delta_time:.2f} seconds to get the info.\n")
    
    # Print the directory tree
    print_tree(tree, tab_string=args.tab_string)
    download_eclass = str(input("\n\n[?] Do you want to download the files of the subject to your local machine? [Y/n] "))
    if 'Y' in download_eclass.upper():
        download_location = str(input(f"[/] Where should the files get downloaded? (Default: ~/Desktop/{course_title}): "))
        print()
        if download_location == '': 
            download_files(all_info, f"~/Desktop/{course_title}")
        else:
            download_files(all_info, download_location)