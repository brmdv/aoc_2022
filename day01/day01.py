def parse_lists(file):
    with open(file, "r") as f:
        subtotal = 0
        for line in f.readlines():
            if line.strip() == "":
                yield subtotal
                subtotal = 0
            else:
                subtotal += int(line.strip())
        yield subtotal


def most_calories(file):
    return max(parse_lists(file))


def calories_top_3(file):
    return sum(sorted(parse_lists(file))[-3:])


def test_example_1():
    assert most_calories("data/example.txt") == 24000


def test_example_2():
    assert calories_top_3("data/example.txt") == 45000


if __name__ == "__main__":
    result_1 = most_calories("data/input1.txt")
    print(f"result 1 = {result_1}")
    result_2 = calories_top_3("data/input1.txt")
    print(f"result 1 = {result_2}")
