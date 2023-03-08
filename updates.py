from src.tree_utils import *
url = "https://eclass.aueb.gr/modules/document/?course=INF117"
list_needed = gen_subtree(url)
print(list_needed)

import os
import urllib.request

def download_files(url_list, base_path="."):
    """
    Download files from a list of URLs and create required folder structure.

    Args:
        url_list (list): A list of URLs to download.
        base_path (str): The base directory to download the files to.
    """
    for url_item in url_list:
        if isinstance(url_item, str):  # it's a URL to a file
            # get the directory path and filename from the URL
            path, filename = os.path.split(url_item)
            # construct the local path to save the file
            local_path = os.path.join(base_path, path)
            # create the directory structure if it doesn't exist
            os.makedirs(local_path, exist_ok=True)
            # download the file
            urllib.request.urlretrieve(url_item, os.path.join(local_path, filename))
        elif isinstance(url_item, list):  # it's a nested list, recurse
            download_files(url_item, base_path)
download_files(list_needed)