def solve(data):
    filesystem = dict()
    path = list()
    stream = iter(data.splitlines())
    while True:
        try:
            current = next(stream)
        except StopIteration:
            break
        args = current.split()
        if args[0] == "$":
            cmd = args[1]
            if cmd == "cd":
                dest = args[2]
                if dest == "..":
                    path.pop()
                elif dest == "/":
                    path = list()
                else:
                    path.append(dest)
            elif cmd == "ls":
                continue
        else:
            size, name = args
            size = None if size == "dir" else int(size)
            add_file(filesystem, path, name, size)

    sizes = list(iter_filesystem("/", filesystem))
    small_directories = [(k, v) for k, v in sizes if v <= 100000]

    total_size = sum(v for _, v in small_directories)

    total_space = 70000000
    unused_space = total_space - max(v for _, v in sizes)
    needed = 30000000
    threshold = needed - unused_space

    candidates = [(k, v) for k, v in sizes if v >= threshold]
    best = next(v for k, v in sorted(candidates, key=lambda x: x[1]))

    return total_size, best


def add_file(parent, path, name, size=None):
    for part in path:
        parent = parent[part]
    parent[name] = size if size is not None else dict()


def get_size(value):
    if isinstance(value, int):
        return value
    return sum(get_size(v) for v in value.values())


def iter_filesystem(name, directory):
    yield name, get_size(directory)
    for k, v in directory.items():
        if isinstance(v, dict):
            for item in iter_filesystem(k, v):
                yield item
