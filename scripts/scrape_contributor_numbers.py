from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests


def get_repo_owner_and_name(repo_url):
    parsed_url = urlparse(repo_url)
    path_components = parsed_url.path.split('/')
    owner = path_components[-2]
    repo = path_components[-1]
    return owner, repo


def text_to_integer(text):
    cleaned_text = text.replace(',', '').replace('.', '')
    try:
        number = int(cleaned_text)
        return number
    except ValueError:
        raise ValueError(
            "Error: Unable to contributor number text to integer."
        )


def get_contributors_count(repo_url):
    repo_owner, repo_name = get_repo_owner_and_name(repo_url)
    response = requests.get(repo_url)
    if response.status_code != 200:
        raise requests.HTTPError("Failed to retrieve repository page.")
    soup = BeautifulSoup(response.text, 'html.parser')
    contributors_count_element = soup.find(
        'a', href=f"/{repo_owner}/{repo_name}/graphs/contributors"
    )
    if contributors_count_element is None:
        raise ValueError("Contributors count not found.")
    num_contributors_text = (
        contributors_count_element.find('span').text.strip())
    num_contributors = text_to_integer(num_contributors_text)
    return num_contributors


def get_contributors_counts(repo_urls):
    counts = [get_contributors_count(repo_url) for repo_url in repo_urls]
    return counts


def main():
    # Do testowania
    try:
        repo_urls = [
            "https://github.com/Kitware/CMake",
            "https://github.com/psf/requests"
        ]
        contributors_counts = get_contributors_counts(repo_urls)
        print(contributors_counts)
    except (requests.HTTPError, ValueError) as error:
        print(str(error))


if __name__ == "__main__":
    main()
