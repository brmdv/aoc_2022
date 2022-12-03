from string import ascii_letters
from typing import Iterator, Sequence

from pytest import mark


def get_common_items(rucksack: str) -> set[str]:
    length = len(rucksack.strip())
    a = set(rucksack[: length // 2])
    b = set(rucksack[length // 2 : length])
    return a & b


def get_item_priority(item: str) -> int:
    return ascii_letters.find(item) + 1


def get_total_priority(rucksack: str) -> int:
    return sum(map(get_item_priority, get_common_items(rucksack)))


def find_common_of_three(r1: str, r2: str, r3: str) -> str:
    common = set(r1.strip()) & set(r2.strip()) & set(r3.strip())
    assert len(common) == 1
    return common.pop()


def chunk_sequence(seq: Sequence, size: int) -> Iterator[Sequence]:
    for i in range(len(seq) // size):
        yield seq[i * size : (i + 1) * size]
    if r := len(seq) % size:
        yield seq[-(len(seq) % size) :]


def get_file_total(file: str) -> int:
    with open(file, "r") as f:
        total = sum(
            get_item_priority(find_common_of_three(*rucksacks))
            for rucksacks in chunk_sequence(f.readlines(), 3)
        )
    return total


# TESTS
def test_common_items():
    assert get_common_items("abcDEFdDFAef") == {"D", "F"}
    assert get_common_items("aaAA") == set()


def test_item_priority():
    assert get_item_priority("a") == 1
    assert get_item_priority("A") == 27
    assert get_item_priority("Z") == 52


def test_example_1():
    with open("data/example.txt", "r") as f:
        total = sum(get_total_priority(line) for line in f.readlines())
    assert total == 157


@mark.parametrize(
    "rucksacks, expected",
    [
        (
            (
                "vJrwpWtwJgWrhcsFMMfFFhFp",
                "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
                "PmmdzqPrVvPwwTWBwg",
            ),
            "r",
        ),
        (
            (
                "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
                "ttgJtRGJQctTZtZT",
                "CrZsJsPPZsGzwwsLwLmpwMDw",
            ),
            "Z",
        ),
    ],
)
def test_common_of_three(rucksacks: tuple[str, str, str], expected: str):
    assert find_common_of_three(*rucksacks) == expected


def test_chunk_sequence():
    assert list(chunk_sequence([1, 2, 3, 4, 5, 6, 7], 2)) == [
        [1, 2],
        [3, 4],
        [5, 6],
        [7],
    ]
    assert list(chunk_sequence([*range(1, 7)], 3)) == [[1, 2, 3], [4, 5, 6]]


def test_example_2():
    assert get_file_total("data/example.txt") == 70


if __name__ == "__main__":
    with open("data/input.txt", "r") as f:
        result1 = sum(get_total_priority(rucksack) for rucksack in f.readlines())
    print(f"{result1 = }")

    result2 = get_file_total("data/input.txt")
    print(f"{result2 = }")
