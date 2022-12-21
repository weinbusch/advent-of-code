import os
import importlib.util
from pathlib import Path
from utils import timing


def main():
    filepaths = list(reversed(sorted(get_filepaths(), key=os.path.getmtime)))
    solvers = collect_solvers(filepaths)
    run_solvers(solvers, most_recent_only=True)


def get_filepaths():
    excluded = ["venv", ".cache", ".config", ".upm", "__pycache__"]
    for dirpath, dirnames, filenames in os.walk(".", topdown=True):
        dirnames[:] = [d for d in dirnames if d not in excluded]
        for f in filenames:
            if f.endswith(".py") and f.startswith("day"):
                yield os.path.join(dirpath, f)


def load_module(filepath):
    root, ext = os.path.splitext(filepath)
    name = ".".join(os.path.split(os.path.relpath(root)))
    spec = importlib.util.spec_from_file_location(name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def collect_solvers(filepaths):
    modules = [load_module(f) for f in filepaths]
    return [(f, m.solve) for f, m in zip(filepaths, modules) if hasattr(m, "solve")]


def run_solvers(solvers, pattern="", most_recent_only=False):
    for f, solver in solvers[:1] if most_recent_only else solvers:
        if solver.__module__.startswith(pattern):
            name = solver.__module__
            data = read_input(f)
            print("\n=====\n")
            print(name)
            print()
            with timing():
                result = solver(data)
                if result:
                    p1, p2 = result
                    print(p1)
                    print(p2)
                print()


def read_input(path):
    root, _ = os.path.splitext(path)
    path = root + ".txt"
    data = ""
    try:
        with open(path, "r") as f:
            data = f.read()
    except FileNotFoundError:
        Path(path).touch()
    return data


if __name__ == "__main__":
    main()
