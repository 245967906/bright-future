import argparse
import os
import random
import re
import string

import pandas
import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("url", help="")
args = parser.parse_args()

baseurl = os.path.dirname(args.url) + "/"
letters = string.ascii_lowercase + string.digits
headers = {
    "Referer": baseurl,
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6)",
}
data = []

r = requests.get(args.url, headers=headers)
soup = BeautifulSoup(r.text, "html.parser")
building_links = [
    baseurl + x.attrs["href"] for x in soup.find_all(name="a", title=None)
    if "building.aspx" in x.attrs["href"]
]

branch_links = []
for link in building_links:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    branch_links += [
        baseurl + x.attrs["href"]
        for x in soup.select("#divShowBranch")[0].find_all(name="a")
    ]

for link in branch_links:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    branch_name = soup.select("#curAddress")[0].text.split("\xa0")[-1]
    house_links = [
        baseurl + x.attrs["href"]
        for x in soup.find_all(name="a", class_="presale2like")
    ]
    houses = []
    for i, url in enumerate(house_links):
        suffix = "".join([random.choice(letters) for x in range(24)])
        headers["Cookie"] = "ASP.NET_SessionId=%s" % suffix
        r = requests.get(url, headers=headers)
        number = re.search(r"房号.*?(\d+)", r.text, re.DOTALL).group(1)
        floor = number[:-2]
        price = re.search(
            r"拟售价格.*?(\d+\.\d+)元/平方米",
            r.text,
            re.DOTALL,
        ).group(1)
        house = {
            "floor": int(floor),
            "number": int(number),
            "price": float(price)
        }
        houses.append(house)
        print(house)
    data.append({"name": branch_name, "houses": houses})

for branch in data:
    df = pandas.DataFrame(branch["houses"])
    df.to_excel(branch["name"] + ".xlsx", index=False)
