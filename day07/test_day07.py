import pytest
import day07 as lib


@pytest.fixture
def example_listing() -> str:
    return """- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)"""


@pytest.fixture
def example_shell_output() -> str:
    return """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


@pytest.fixture
def basic_file_system() -> lib.Directory:
    root = lib.Directory("/")
    file_1 = lib.File("a.txt", 500, parent=root)
    dir_1 = lib.Directory("my_dir", parent=root)
    file_2 = lib.File("b.txt", 800, parent=dir_1)
    return root


def test_filestystem_creation(basic_file_system: lib.Directory):
    assert len(basic_file_system._contents) == 2


def test_directory_size(basic_file_system: lib.Directory):
    assert basic_file_system.size == 1300


@pytest.fixture
def example_file_system(example_listing: str):
    directory = lib.parse_listing(example_listing)
    assert directory.name == "/"
    assert directory.size == 48381165
    return directory


def test_walk(basic_file_system):
    assert len([*lib.walk(basic_file_system)]) == 4


def test_walk_and_get_root(example_file_system: lib.Directory):
    for node in lib.walk(example_file_system):
        assert example_file_system == node.get_root()


def test_get_sizes_example(example_listing: str):
    filesystem = lib.parse_listing(example_listing)
    assert sum(lib.get_directory_sizes(filesystem)) == 95437


def test_import_shell(example_shell_output: str, example_file_system: lib.Directory):
    shell_dir = lib.read_shell_history(example_shell_output)
    for node_1, node_2 in zip(lib.walk(shell_dir), lib.walk(example_file_system)):
        assert node_1.name == node_2.name


def test_example_2(example_file_system):
    assert lib.part_2(example_file_system) == 24933642
