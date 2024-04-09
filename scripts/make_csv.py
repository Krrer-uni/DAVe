import collections
import os
import re

import pandas as pd


def find_dependencies(package_name: str) -> list[str]:
    filename = os.path.join("..", "data", "packages", f"{package_name}.rb")
    dependencies: list[str] = []
    try:
        with open(filename, "r") as file:
            for line_number, line in enumerate(file, start=1):
                prefix = re.search(' *depends_on "', line)
                if prefix:
                    start = line[prefix.end() :]
                    suffix = re.search('"', start)
                    if suffix:
                        word = start[: suffix.start()]
                        dependencies.append(word)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    return dependencies


# print(find_dependencies(package_name=package_name))


def get_dependency_tree(package_name: str) -> tuple[set, set]:
    relations = set()
    processed = set()
    dep_queue = collections.deque()
    dep_queue.append(package_name)
    while len(dep_queue) != 0:
        package = dep_queue.pop()
        if package in processed:
            continue
        processed.add(package)
        for dep in find_dependencies(package):
            relations.add((package, dep))
            dep_queue.append(dep)

    return processed, relations


def get_csv(package_name: str):
    processed, relations = get_dependency_tree(package_name)
    df = pd.DataFrame(list(relations))
    df.rename(columns={0: "package", 1: "dependency"}, inplace=True)
    df.to_csv("../data/csv/" + package_name + ".csv", index=False)
