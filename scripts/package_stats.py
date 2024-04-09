import math
import os
import re

import pandas as pd
import requests

def get_analytics(category):
    url = f"https://formulae.brew.sh/api/analytics/{category}/homebrew-core/365d.json"
    data = requests.get(url).json()

    packages = {}
    for name, pkg in data["formulae"].items():
        packages[name] = pkg[0]["count"]
    return packages

install = get_analytics("install")
install_on_request = get_analytics("install-on-request")

def get_stats_for_package(pkg):
    with open(f"../data/packages/{pkg}.rb") as f:
        data = f.read()
    head = re.search(r'head "([^"]*)"', data)
    if head is not None:
        head = head.group(1)
    else:
        head = ""
    install_count = install.get(pkg, math.nan)
    on_request_count = install_on_request.get(pkg, math.nan)
    return pkg, head, install_count, on_request_count

packages = os.listdir("../data/packages")
packages = [p[:-3] for p in packages] # Strip the ".rb" suffix
packages = [get_stats_for_package(p) for p in packages]

df = pd.DataFrame(packages)
df.rename(columns={0: "package", 1: "repo_url", 2: "install", 3: "install-on-request"}, inplace=True)
df.to_csv("../data/csv/package_stats.csv", index=False)