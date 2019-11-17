import csv
import os
from io import StringIO
import re
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore


init(autoreset=True)
url = "https://docs.google.com/spreadsheets/d/19RED1ZRvHMLfjITdwYfm5xko3FZtMkh7uPA7oqLcg9A/export?format=csv&id=19RED1ZRvHMLfjITdwYfm5xko3FZtMkh7uPA7oqLcg9A&gid=0"
res =  requests.get(url)



xmlfile = os.path.join(os.path.dirname(__file__), '..', 'NanopesosEN.html')
output_file = os.path.join(os.path.dirname(__file__), '..', 'NanopesosEO.html')
with open(xmlfile) as fp:
    soup = BeautifulSoup(fp, 'html.parser')

title = soup.find_all("title")[0]
title.string = "NanopesosEO"

def get_passages(soup):
    passages = {}
    for passage in soup.find_all("tw-passagedata"):
        passages[passage['name']] = passage
    return passages

reader = csv.reader(StringIO(res.content.decode('utf-8')), delimiter=',')
passages = get_passages(soup)
ids = list(passages.keys())
ids.sort()
print(Fore.YELLOW + str(ids))
next(reader) # Header
for row in reader:
    name = row[0]
    hud = row[1]
    spanish = row[2]
    esperanto = row[4]
    # print(Fore.GREEN + esperanto)

    if name == 'notificación en tu celular2':
        continue

    hud = hud.replace("Dinero", "Mono")
    hud = hud.replace("Día ", "Tago ")
    if hud:
        hud += "\n"
    passage = passages[name]
    # print(Fore.RED + str(passage))

    if not esperanto:
        continue
    passage.string = hud + esperanto
    print(name)

    es_links = [r.split('|')[-1] for r in re.findall('\[\[([^\[\]]*)\]\]', spanish)]
    eo_links = [r.split('|')[-1] for r in re.findall('\[\[([^\[\]]*)\]\]', esperanto)]
    if es_links != eo_links:
        print(es_links, eo_links)
    assert es_links == eo_links

with open(output_file, "wb") as file:
    file.write(soup.encode(formatter="html"))