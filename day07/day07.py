from typing import Iterator, Optional

import re


class Node:
    def __init__(self, name: str, parent: Optional["Directory"] = None) -> None:
        self.name = name
        self._parent: Optional[Directory] = None

        if parent is not None:
            self.put_in_dir(parent)

    def put_in_dir(self, directory: "Directory") -> None:
        if self._parent != directory and self != directory:
            self._parent = directory
            directory.add_child(self)

    @property
    def parent(self) -> Optional["Directory"]:
        return self._parent

    def get_root(self) -> "Directory":
        if self.parent is not None:
            return self.parent.get_root()
        else:
            return self  # type:ignore[return-value]


class File(Node):
    def __init__(
        self, name: str, size: int, parent: Optional["Directory"] = None
    ) -> None:
        super().__init__(name, parent)
        self.size = size

    def __repr__(self) -> str:
        return f"<FILE: {self.name} ({self.size})>"


class Directory(Node):
    def __init__(self, name: str, parent: Optional["Directory"] = None) -> None:
        super().__init__(name, parent)
        self._contents: list[Node] = []

    @property
    def size(self) -> int:
        return sum(child.size for child in self._contents)  # type:ignore[attr-defined]

    def add_child(self, node: Node) -> None:
        if not node in self._contents:
            self._contents.append(node)
            node.put_in_dir(self)

    def __repr__(self) -> str:
        return f"<DIR: {self.name}>"

    @property
    def contents(self) -> list[Node]:
        return self._contents

    def ls(self) -> set[str]:
        return set(c.name for c in self._contents)

    def get_child(self, name: str) -> Optional[Node]:
        for child in self._contents:
            if child.name == name:
                return child
        return None


def parse_listing(listing: str) -> Directory:
    parent_dir = None
    parent_level = 0
    pattern = re.compile(
        r"(?P<indent> *)- (?P<name>.*?) \((?P<type>dir|file)(, size=(?P<size>[0-9]+))?\)"
    )
    for line in listing.splitlines():
        if (m := re.match(pattern, line)) is not None:
            level = len(m.group("indent")) // 2
            while parent_level >= level and parent_dir is not None:
                parent_dir = parent_dir.parent
                parent_level -= 1

            match m.group("type"):
                case "dir":
                    parent_dir = Directory(name=m.group("name"), parent=parent_dir)
                    parent_level = level
                case "file":
                    File(
                        name=m.group("name"),
                        size=int(m.group("size")),
                        parent=parent_dir,
                    )

    return parent_dir.get_root()  # type:ignore


def walk(d: Directory, nodes: Optional[list[Node]] = None) -> list[Node]:
    nodes = nodes or [d]
    for child in d.contents:
        if isinstance(child, Directory):
            nodes.extend(walk(child))
        else:
            nodes.append(child)
    return nodes


def get_directory_sizes(
    directory: Directory, min_size: int = 0, max_size: int = 100000
) -> list[int]:
    return list(
        filter(
            lambda x: min_size <= x <= max_size,
            (d.size for d in walk(directory) if isinstance(d, Directory)),
        )
    )


def read_shell_history(history: str) -> Directory:
    cwd: Directory = None  # type:ignore
    in_listing_output = False
    for line in history.splitlines():
        if line.startswith("$"):
            in_listing_output = False
            args = line.split(" ")
            match args[1]:
                case "cd":
                    if cwd is None:
                        cwd = Directory(name=args[2])
                    elif args[2] == "..":
                        cwd = cwd.parent
                    else:
                        if args[2] in cwd.ls() and isinstance(
                            new_dir := cwd.get_child(args[2]), Directory
                        ):
                            cwd = new_dir
                        else:
                            cwd = Directory(name=args[2], parent=cwd)
                case "ls":
                    in_listing_output = True
        else:
            if in_listing_output:
                args = line.split(" ")
                if args[0] == "dir":
                    if args[1] not in cwd.ls():
                        Directory(name=args[1], parent=cwd)
                else:
                    File(args[1], size=int(args[0]), parent=cwd)

    return cwd.get_root()


def part_2(root: Directory, total_space: int = 70_000_000, min_space=30_000_000) -> int:
    available_space = total_space - root.size
    target_free = min_space - available_space
    return min(get_directory_sizes(root, min_size=target_free, max_size=total_space))


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input_history = f.read()
    filesystem = read_shell_history(input_history)

    answer_1 = sum(get_directory_sizes(filesystem))
    print(f"{answer_1 = }")

    answer_2 = part_2(filesystem)
    print(f"{answer_2 = }")
