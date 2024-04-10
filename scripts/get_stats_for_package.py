import sys

from scripts.make_dependency_graph import get_csv


if __name__ == "__main__":
    package_name = sys.argv[1]
    get_csv(package_name)
