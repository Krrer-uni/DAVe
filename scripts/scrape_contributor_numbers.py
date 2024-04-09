import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pandas.core.generic import DtypeArg

script_dir = os.path.dirname(__file__)
csv_dir = Path(script_dir).parent / "data" / "csv"


def get_repo_owner_and_name(repo_url: str) -> tuple[str, str]:
    repo_url = repo_url.removesuffix(".git")
    parsed_url = urlparse(repo_url)
    path_components = parsed_url.path.split("/")

    owner = path_components[-2]
    repo = path_components[-1]

    return owner, repo


def text_to_integer(text: str) -> int:
    cleaned_text = text.replace(",", "").replace(".", "")
    try:
        number = int(cleaned_text)
        return number
    except ValueError:
        raise ValueError("Error: Unable to contributor number text to integer.")


def get_contributors_count(repo_url: str) -> int | None:
    if "github.com" not in repo_url:
        print("Error: Repository URL is not from GitHub.")
        return None

    repo_owner, repo_name = get_repo_owner_and_name(repo_url)

    response = requests.get(repo_url)
    if response.status_code != 200:
        print(f"Failed to retrieve repository page for {repo_url}.")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Link can have different letter cases than the URL
    contributors_count_elements = soup.find_all(
        lambda tag: tag.name == "a"
        and "href" in tag.attrs
        and tag["href"].lower()
        == f"/{repo_owner.lower()}/{repo_name.lower()}/graphs/contributors"
    )

    if len(contributors_count_elements) == 0:
        print(f"Contributors count not found for {repo_url}.")
        return None

    num_contributors_text = contributors_count_elements[0].find("span").text.strip()
    num_contributors = 0

    if num_contributors_text[-1] == "+":
        num_contributors_text = contributors_count_elements[1].get_text(strip=True)[
            2:-13
        ]
        num_contributors += 14
    try:
        num_contributors = text_to_integer(num_contributors_text)
    except ValueError as error:
        print(f"Error: {error}")
        return None

    # print(f"{repo_url}: {num_contributors}")
    return num_contributors


def get_contributors_counts(repo_urls):
    counts = [get_contributors_count(repo_url) for repo_url in repo_urls]
    return counts


dtypes: DtypeArg = {
    "package": str,
    "repo_url": str,
    "install": "Int64",
    "install_on_request": "Int64",
}


def test_get_contributors_count():
    try:
        repo_urls = [
            # "https://github.com/Kitware/CMake",
            # "https://github.com/psf/requests",
            # "https://github.com/Homebrew/homebrew-core",
            # "https://github.com/Krrer-uni/DAVe",
            # "https://github.com/freeCodeCamp/freeCodeCamp.git",
            # "https://github.com/OSGeo/proj",
            # "https://github.com/google/googletest",
        ]
        contributors_counts = get_contributors_counts(repo_urls)
        print(contributors_counts)
    except (requests.HTTPError, ValueError) as error:
        print(str(error))


# Use a list to hold the counter so it can be modified inside the function
counter = [0]


def wrapped_get_contributors_count(url, total):
    result = get_contributors_count(url) if url == url else None
    print(f"Processed row {counter[0]+ 1}/{total}")
    counter[0] += 1
    return result


def append_contributor_count(row, total_rows, out_file):
    row["contributors_count"] = wrapped_get_contributors_count(
        row["repo_url"], total_rows
    )
    row_df = pd.DataFrame([row])
    row_df.to_csv(out_file, mode="a", header=not os.path.exists(out_file), index=True)


def main(start_index=0):
    counter[0] = start_index
    df = pd.read_csv(csv_dir / "package_stats.csv", dtype=dtypes)
    total_rows = df.shape[0]
    out_file = csv_dir / "package_stats_with_contributors.csv"

    if start_index == 0 and os.path.exists(out_file):
        os.remove(out_file)

    for index, row in df.iterrows():
        if index >= start_index:
            append_contributor_count(row, total_rows, out_file)

    print(f"Data saved to {out_file}")


if __name__ == "__main__":
    start_from = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    main(start_from)
