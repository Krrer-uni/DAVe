import collections

import pandas as pd
import re

package_name = "cmake"


def find_dependencies(package_name: str) -> []:
    filename = "../data/packages/" + package_name + ".rb"
    dependencies = []
    try:
        with open(filename, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                prefix = re.search(" *depends_on \"", line)
                if prefix:
                    start = line[prefix.end():]
                    suffix = re.search("\"", start)
                    if suffix:
                        word = start[:suffix.start()]
                        dependencies.append(word)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    return dependencies


print(find_dependencies(package_name=package_name))

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

print(len(relations))
df =pd.DataFrame(list(relations))
df.rename(columns={0: "package", 1: "dependency"}, inplace=True)
df.to_csv("../data/csv/" + package_name + ".csv", index=False)