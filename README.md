# tree-eclass
## _Eclass File Downloading and File Finder_

tree-eclass is a python project used for auto-updating and downloading the latest 
files and folders for a subject from eclass

## Features

- Auto-update course folder
- Command line tree of subject's files and folders

## Installation

tree-eclass requires [Python3](https://python.org/) to run.

Install the required libraries.

```sh
git clone https://github.com/panagiotisppg/tree-eclass.git
cd tree-eclass
pip3 install -r requirements.txt
```
Run the program:
```sh
python3 main.py -C XXXYYY
```
````Where XXXYYY is the course number. For example: INF123````
##### Auto-Update Featue
You can get alerts in the alerts.csv file for new files uploaded to your subscribed courses
by running the updates python file
```sh
python3 updates.py
```
##### Warning
This code in it's current version is only used for public [eclass](https://eclass.aueb.gr) classes
