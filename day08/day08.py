import numpy as np


class TreeGrid:
    def __init__(self, contents: str) -> None:
        self.grid = np.array(
            [[int(char) for char in line] for line in contents.split("\n")]
        )
