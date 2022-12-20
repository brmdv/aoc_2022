import pytest
import day08 as lib


@pytest.fixture
def example_forest() -> lib.TreeGrid:
    return lib.TreeGrid(
        """30373
25512
65332
33549
35390"""
    )


def test_grid_creation(example_forest: lib.TreeGrid):
    assert example_forest.grid.shape == (5, 5)
