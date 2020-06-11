import argparse
import re

import requests
import pandas
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("url", help="")
parser.add_argument("--output", "-o", default="output.xlsx", help="")
args = parser.parse_args()
baseurl = "http://zjj.sz.gov.cn/ris/bol/szfdc/"
r = requests.get(args.url)

soup = BeautifulSoup(r.text, "html.parser")
links = [
    baseurl + x.attrs["href"]
    for x in soup.find_all(name="a", class_="presale2like")
]

houses = []
for link in links:
    r = requests.get(link)
    number = re.search(r"房号.*?(\d+)", r.text, re.DOTALL).group(1)
    floor = number[:-2]
    price = re.search(
        r"拟售价格.*?(\d+\.\d+)元/平方米",
        r.text,
        re.DOTALL,
    ).group(1)
    houses.append({
        "floor": int(floor),
        "number": int(number),
        "price": float(price)
    })
df = pandas.DataFrame(houses)
df.to_excel(args.output, index=False)
