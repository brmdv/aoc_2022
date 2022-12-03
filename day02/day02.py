from enum import Enum

import pytest


class Play(int, Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @classmethod
    def parse(cls, code: str) -> "Play":
        match code.lower().strip():
            case "a" | "x":
                return cls.ROCK
            case "b" | "y":
                return cls.PAPER
            case "c" | "z":
                return cls.SCISSORS
            case _:
                raise AttributeError(f"Could not parse {code}")


class Outcome(int, Enum):
    WON = 6
    LOST = 0
    DRAW = 3

    @classmethod
    def parse(cls, code: str) -> "Outcome":
        match code.lower().strip():
            case "x":
                return cls.LOST
            case "y":
                return cls.DRAW
            case "z":
                return cls.WON
            case _:
                raise AttributeError(f"Could not parse {code}")


def parse_round_original(line: str) -> tuple[Play, Play]:
    opponent, player, *_ = (Play.parse(p) for p in line.split(" "))
    return player, opponent


def play_round(player_play: Play, opponent_play: Play) -> Outcome:
    if player_play == opponent_play:
        return Outcome.DRAW
    else:
        return Outcome.LOST if (player_play - opponent_play) % 3 == 2 else Outcome.WON


def round_score(player_play: Play, opponent_play: Play) -> int:
    return player_play + play_round(player_play, opponent_play)


def total_score(file: str) -> int:
    with open(file, "r") as f:
        total = sum(round_score(*parse_round_original(line)) for line in f.readlines())
    return total


def parse_round_new(line: str) -> tuple[Play, Outcome]:
    opponent, exp_outcome, *_ = line.split(" ")
    return Play.parse(opponent), Outcome.parse(exp_outcome)


def round_score_new(opponent_play: Play, expected_outcome: Outcome) -> int:
    for option in Play:
        if play_round(option, opponent_play) == expected_outcome:
            player_play = option
    return round_score(player_play, opponent_play)


def total_score_new(file: str):
    with open(file, "r") as f:
        total = sum(round_score_new(*parse_round_new(line)) for line in f.readlines())
    return total


# TESTS
def test_parse_line():
    assert Play.parse("A") == Play.ROCK
    assert Play.parse("X") == Play.ROCK
    assert Play.parse("z") == Play.SCISSORS


@pytest.mark.parametrize(
    "player, opponent, expected",
    [
        (Play.PAPER, Play.PAPER, Outcome.DRAW),
        (Play.ROCK, Play.PAPER, Outcome.LOST),
        (Play.PAPER, Play.SCISSORS, Outcome.LOST),
        (Play.SCISSORS, Play.PAPER, Outcome.WON),
    ],
)
def test_round(player: Play, opponent: Play, expected: Outcome):
    assert play_round(player, opponent) == expected


@pytest.mark.parametrize(
    "line, expected",
    [("A Y", 8), ("B X", 1), ("C Z", 6)],
)
def test_score_one_round(line: str, expected: Outcome):
    p, o = parse_round_original(line)
    assert round_score(p, o) == expected


def test_example_1():
    assert total_score("data/example.txt") == 15


@pytest.mark.parametrize(
    "line, expected",
    [("A Y", 4), ("B X", 1), ("C Z", 7)],
)
def test_new_round_notation_score(line: str, expected):
    assert round_score_new(*parse_round_new(line)) == expected


def test_example2():
    assert total_score_new("data/example.txt") == 12


# RESULTS
if __name__ == "__main__":
    result1 = total_score("data/input1.txt")
    print(f"{result1 = }")
    result2 = total_score_new("data/input1.txt")
    print(f"{result2 = }")
