from typing import List
from random import shuffle

"""This module contains the RandomGenerator class.

Classes:
-  RandomGenerator
"""

class RandomGenerator:
    """This class represents a random generator which will be used to
    generate the sequence of tetriminoes spawned in a game of Tetris.
    
    Public Methods:
    - next() -> str
    """
    def __init__(self):
        self._list = ["J", "L", "O", "I", "S", "Z", "T"]
        shuffle(self._list)
        self._index = 0

    def next(self) -> str:
        """Return a string which represents the next tetrimino that
        should be spawned."""
        next_tetrimino = self._list[self._index]
        if self._index == 6: # Reached the end so re-shuffle and reset
            shuffle(self._list)
            self._index = 0
        else:
            self._index += 1
        return next_tetrimino