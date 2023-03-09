import os
import requests

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