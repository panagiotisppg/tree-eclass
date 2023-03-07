from src.GetLinks import get_links
from src.tree import gen_tree

url = "https://eclass.aueb.gr/modules/document/?course=INF111"
# url = "https://eclass.aueb.gr/modules/document/?course=INF371"
# url = "https://eclass.aueb.gr/modules/document/?course=INF195"
# url = "https://eclass.aueb.gr/modules/document/?course=INF404"
gen_tree(url)