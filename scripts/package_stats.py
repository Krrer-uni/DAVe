import math
import os
import re
from pathlib import Path

import pandas as pd
import requests

script_dir = os.path.dirname(__file__)
data_dir = Path(script_dir).parent / "data"
packages_dir = data_dir / "packages"
csv_dir = data_dir / "csv"


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
    with open(packages_dir / f"{pkg}.rb") as f:
        data = f.read()
    head = re.search(r'head "([^"]*)"', data)
    if head is not None:
        head = head.group(1)
    else:
        head = ""
    install_count = install.get(pkg, math.nan)
    on_request_count = install_on_request.get(pkg, math.nan)
    return pkg, head, install_count, on_request_count


def column_to_int_coerce(column: pd.Series) -> pd.Series:
    return pd.to_numeric(column.str.replace(",", ""), errors="coerce")


packages = os.listdir(str(packages_dir))
packages = [p[:-3] for p in packages]  # Strip the ".rb" suffix
packages = [get_stats_for_package(p) for p in packages]

df = pd.DataFrame(
    packages,
)

df.rename(
    columns={0: "package", 1: "repo_url", 2: "install", 3: "install-on-request"},
    inplace=True,
)


df["install"] = column_to_int_coerce(df["install"]).astype("Int64")
df["install-on-request"] = column_to_int_coerce(df["install-on-request"]).astype(
    "Int64"
)


df.to_csv(
    csv_dir / "package_stats.csv",
    index=False,
)
