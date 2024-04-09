# DAVe - Dependency Atack VEctor finder

## Usage

Firstly unpack the dataset. Run from project root dir:

```bash
./scripts/unpack.sh
```

To get dependency graph data: (output in `data/csv/dependencies.csv`)

```bash
python3 ./scripts/make_dependency_graph.py
```

To get package stats: (output in `data/csv/package_stats.csv`)

```bash
python3 ./scripts/package_stats.py
```
