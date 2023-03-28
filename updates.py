from datetime import datetime
import time
from src.downloading import *
from src.GetLinks import *
from src.tree_utils import *




update_scanner_delay_in_seconds = 5*60
# Every 5 minutes the program will check for updates in the subscribed courses

home = os.getcwd()

with open('subscribed.txt', 'r') as file:
     courses, paths = [], []
     lines = file.read().split('\n')[1:]
     for line in lines:
          if line != '' or line != '\n':
               course = line.split(' ')[0];     courses.append(course)
               path = ' '.join(line.split(' ')[1:]);     paths.append(path)
file.close()

while True:
     for i in range(len(courses)):
          new = []
          course = courses[i]
          path = paths[i]
          response = requests.get(f"https://eclass.aueb.gr/courses/{course}/");    soup = BeautifulSoup(response.content, 'html.parser');    h1_tag = soup.find('h1', class_='page-title');    course_title = h1_tag.text.strip()
          url = f"https://eclass.aueb.gr/modules/document/?course={course} {course_title} d"

          tree = gen_subtree(url, print_enabled=False)
          print_tree(tree, tab_string='', print_enabled=False)

          new = download_files(all_info, path,getting_updates=True, print_enabled=False)

          all_info.clear()
          os.chdir(home)

          if len(new) > 0:
               with open('alerts.csv', 'a') as file2:
                    for update in new:
                         file2.write(f"{course_title},{course},'{str(update).split('/')[-1]}',{datetime.now()}\n")
               file2.close()

     time.sleep(update_scanner_delay_in_seconds)