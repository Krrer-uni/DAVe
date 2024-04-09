import collections
import os

import pandas as pd
import re

def find_dependencies(package_name: str) -> []:
    filename = "../data/packages/" + package_name + ".rb"
    dependencies = []
    try:
        with open(filename, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                if ":build" in line or ":test" in line:
                    continue # Skip dependencies that end users don't need
                prefix = re.search("(depends_on \")|(uses_from_macos \")", line)
                if prefix:
                    start = line[prefix.end():]
                    suffix = re.search("\"", start)
                    if suffix:
                        word = start[:suffix.start()]
                        dependencies.append(word)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    return dependencies


# print(find_dependencies(package_name=package_name))


def get_dependency_tree(package_name: str) -> [set, set]:
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



def get_full_csv():
    packages = os.listdir("../data/packages")
    packages = [p[:-3] for p in packages] # strip ".rb"
    relations = []
    for pkg in packages:
        deps = find_dependencies(pkg)
        for d in deps:
            relations.append((pkg,d))

    df = pd.DataFrame(list(relations))
    df.rename(columns={0: "package", 1: "dependency"}, inplace=True)
    df.to_csv("../data/csv/dependencies.csv", index=False)




if __name__ == "__main__":
    get_full_csv()